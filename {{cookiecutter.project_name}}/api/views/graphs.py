"""
The front end uses a certain library for graphs and tables plotting.
this class along with the TablesBuilder object are used to get the data, filter and format as easily as we can
and also export it to CSV.
"""
import pandas as pd
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Farm, FarmScores
from common.base.exceptions import (FarmIdNotSupplied, LevelIsMissingException, TableIdNotProvided,
                                    LevelMaxAllowedItemsError, IdsNotProvided, GroupNotFound)
from common.base.views import ScrListViewSet
from common.consts import (ID, FARM, BRANCH, LEVEL, FARM_ID, RelatedNames, GROUP, DATE, NAME,
                           SYSTEM_KEY, POPULATION, TABLE, TABLE_NAME)
from common.dates.consts import TWO_DAYS_AGO
from common.dates.request_handler import request_dates_handler
from common.dates.utils import construct_dates_dict, get_mock_df
from common.docs import STATS_DOCS, DocsParams, EXPORT_TO_CSV_DOCS, CSV_EXPORT
from common.tables import TablesBuilder, tables_builder


class GraphsView(ScrListViewSet):
    serializer_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._kpis = None
        self._graph_builder: TablesBuilder = None  # noqa

    @property
    def graph_builder(self):
        # set the dates filtering
        kpis_names_list = []  # in some applications it's dynamic in some it's static
        return tables_builder({kpi: [DATE, kpi] for kpi in kpis_names_list}, days=self.days, end_date=self.end_date)

    @extend_schema(description='get a list of all farms associated with the user and their branches and groups',
                   summary='Groups And Branches By Farms', parameters=[DocsParams.META_FARM_ID])
    def list(self, request, *args, **kwargs):
        farm_id = request.query_params.get(FARM_ID, None)
        if farm_id is None:
            raise FarmIdNotSupplied
        else:
            queryset = Farm.objects.get(user__in=self.request.user, id=farm_id)
            serializer = self.get_serializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @property
    def get_queryset(self):
        self.days, self.dates_range, self.end_date = request_dates_handler(self.request, default_end_date=TWO_DAYS_AGO)

        self.level = self.request.query_params.get(LEVEL, None)

        if self.level is None:
            raise LevelIsMissingException

        self.farm_ids = self.request.query_params.get(FARM_ID, None)

        if self.farm_ids is None:
            raise FarmIdNotSupplied

        self.farm_ids = self.farm_ids.split(',')

        if self.level == FARM:
            return Farm.objects.filter(account__account_users=self.request.user, id__in=self.farm_ids). \
                prefetch_related(Prefetch(lookup=RelatedNames.FARM_SCORES,
                                          queryset=FarmScores.objects.filter(date__range=self.dates_range)),
                                 ).only(NAME, ID, SYSTEM_KEY)

        else:
            if len(self.farm_ids) > 1:
                raise LevelMaxAllowedItemsError
            # used if there's another levels in the app (groups/ branches...)
            self.ids = self.request.query_params.get(ID, None)
            if self.ids is None:
                raise IdsNotProvided
            self.ids = self.ids.split(',')

    @extend_schema(summary='Graphs Data', description=STATS_DOCS,
                   parameters=[DocsParams.ID, DocsParams.LEVEL, DocsParams.START_DATE, DocsParams.END_DATE,
                               DocsParams.FARM_ID, DocsParams.TABLE_NAME])
    @action(detail=False)
    def get_stats(self, request, *args, **kwargs):
        level = self.request.query_params.get(LEVEL, None)
        if level is None:
            raise LevelIsMissingException

        table = request.query_params.get(TABLE, None)
        table_name = request.query_params.get(TABLE_NAME, None)

        data = self._level_dispatcher(as_exporter=False, level=level, table_id=table, table_name=table_name)
        return Response(data)

    @extend_schema(summary="Export To CSV", description=EXPORT_TO_CSV_DOCS, responses=CSV_EXPORT,
                   parameters=[DocsParams.TABLE, DocsParams.ID, DocsParams.LEVEL, DocsParams.START_DATE,
                               DocsParams.END_DATE, DocsParams.FARM_ID])
    @action(detail=False)
    def export_to_csv(self, request, *args, **kwargs):
        self.days, self.dates_range, self.end_date = request_dates_handler(self.request, default_end_date=TWO_DAYS_AGO)
        level = request.query_params.get(LEVEL, None)
        if level is None:
            raise LevelIsMissingException

        table = request.query_params.get(TABLE, None)
        if table is None:
            raise TableIdNotProvided
        return self._level_dispatcher(as_exporter=True, level=level, table_name=table)

    def _level_dispatcher(self, as_exporter, level, table_id=None, table_name=None):
        """
        given the desired level of KPIs and if as csv exporter or graph builder returns the proper method
        """
        query = self.get_queryset

        if as_exporter is True and table_name is None and table_id is None:
            raise TableIdNotProvided

        else:
            # get desired level's kpis
            if level == FARM:
                return self._farms_level_constructor(query=query, as_exporter=as_exporter, table=table_id,
                                                     table_name=table_name)
            # Example use
            elif level == BRANCH:
                return self._branches_level_constructor(query=query, as_exporter=as_exporter, table_name=table_name)

            elif level == GROUP:
                return self._groups_level_constructor(query=query, as_exporter=as_exporter, table_name=table_name)

    def _farms_level_constructor(self, query, as_exporter, table=None, table_name=None):
        if len(self.farm_ids) == 1:
            if as_exporter is True:
                # one farm and to export to CSV
                farm = query.get(id=self.farm_ids[0])
                query = farm.farm_scores
                return self.graph_builder.export_to_csv(query=query, table=table_name,
                                                        fields_names=(table_name, DATE, NAME, POPULATION),
                                                        farm_name=farm.name)
            else:
                # if only one farm is specified and not as CSV
                return self._farm_graph_constructor(farm_id=self.farm_ids[0], query=query, table=table,
                                                    table_name=table_name)

        else:
            thresholds = self.request.user.user_selected_kpis.get_kpis_lower_thresholds()
            # Multiple Farms, reconstruct for comparison will handle automatically if it's an export or graphs
            tables_names = [table_name] if table_name is not None else list(self.graph_builder.graphs.keys())
            name_field = 'farm__name'

            dfs = [pd.DataFrame(farm.farm_scores.values(DATE, *tables_names, name_field))
                   if farm.farm_scores.all().exists() is True
                   else get_mock_df(name_field=name_field, name=farm.name, fields=tables_names,
                                    dates_list=construct_dates_dict(days=self.days, end_date=self.end_date))
                   for farm in query]

            return self.graph_builder.reconstruct_for_comparison(dfs=dfs, as_exporter=as_exporter,
                                                                 name_field=name_field, thresholds=thresholds)

    def _branches_level_constructor(self, query, as_exporter, table_name=None):

        if len(self.ids) == 1:
            return self._branch_graph_constructor(query) if as_exporter is False \
                else self.graph_builder.export_to_csv(query=query[0].branch_scores.all(), table=table_name,
                                                      fields_names=(table_name, DATE, NAME, POPULATION),
                                                      farm_name=query[0].farm.name, branch_name=query[0].name)

        else:
            tables_names = [table_name] if table_name is not None else list(self.graph_builder.graphs.keys())
            name_field = 'branch__name'
            dfs = [pd.DataFrame(branch.branch_scores.all().values(DATE, *tables_names, name_field)) for branch in query]
            return self.graph_builder.reconstruct_for_comparison(dfs=dfs, as_exporter=as_exporter,
                                                                 name_field=name_field)

    def _groups_level_constructor(self, query, as_exporter, table_name=None):
        if len(self.ids) == 1:
            if as_exporter is False:
                return self._group_graph_constructor(query=query, group_number=self.ids[0], not_modify=False)
            else:
                group = query[0]
                return self.graph_builder.export_to_csv(query=group.group_scores.all(), table=table_name,
                                                        fields_names=(table_name, DATE, NAME, POPULATION),
                                                        farm_name=group.branch.farm.name, branch_name=group.name)

        else:
            tables_names = [table_name] if table_name is not None else list(self.graph_builder.graphs.keys())
            name_field = 'group__name'
            dfs = [pd.DataFrame(group.group_scores.all().values(DATE, *tables_names, name_field)) for group in
                   query]
            return self.graph_builder.reconstruct_for_comparison(dfs=dfs, as_exporter=as_exporter,
                                                                 name_field=name_field)

    ############### CONSTRUCTORS ###############
    def _farm_graph_constructor(self, farm_id, query, table, table_name=None):
        # will add this number to each date's dictionary, in order to add a threshold line to the graph
        thresholds: dict = self.kpis.get_kpis_lower_thresholds()
        query = query.get(id=farm_id)
        return self.graph_builder.construct_graphs(replace_name=query.name, ignore_keys=True,
                                                   specific_graph=table, thresholds=thresholds,
                                                   by_table_name=table_name, query=query.farm_scores
                                                   )

    def _branch_graph_constructor(self, query, get_query=False):
        thresholds: dict = self.kpis.get_kpis_lower_thresholds()

        if get_query:
            return query
        else:
            branch = query[0]
            return self.graph_builder.construct_graphs(replace_name=branch.name,
                                                       ignore_keys=True,
                                                       query=branch.branch_scores.all(),
                                                       thresholds=thresholds)

    def _group_graph_constructor(self, query, group_number, not_modify=True):
        thresholds: dict = self.kpis.get_kpis_lower_thresholds()
        if not query.exists():
            raise GroupNotFound
        if not_modify is False:
            group = query[0]
            return self.graph_builder.construct_graphs(replace_name=group.name, ignore_keys=True,
                                                       thresholds=thresholds, query=group.group_scores.all())

        return self.graph_builder.construct_graphs(replace_name=query[0].group.name,
                                                   ignore_keys=True, thresholds=thresholds,
                                                   query=query.filter(group__group_number=group_number)
                                                   )
