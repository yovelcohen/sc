from statistics import mean
from typing import Dict

from django.db.models import Prefetch, Sum, Case, When
from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from base.dates.consts import month_range, TWO_DAYS_AGO
from base_scr.base_views import ScrListViewSet
from base_scr.common.consts import (RelatedNames, COW_COUNT, DATE, SCORE_TYPE, KPIS, MILKING_CATTLE, SYSTEM_KEY, FARM,
                                    SW_VERSION, UTC_OFFSET, TIMEZONE, DEALER_NAME, LAST_SW_UPDATE)
from common.consts import (AVG_SCORE, GREEN, YELLOW, RED, ASSIGNED_TAG_COUNT, FARM_SIZE,
                           SCORE, TREND, SYSTEM_TYPE)
from common.utils import trend, score_type_from_kpi
from configurations.models import FarmConfigurationsLayer, KPI
from consumer_api.docs.serializers import FarmSerializerResponse
from consumer_api.models import Farm, FarmKPIs, BranchKPIs, Branch
from consumer_api.serializers.farm_serializers import FarmSerializer, TilesResponse


class FarmsView(ScrListViewSet):
    serializer_class = FarmSerializer

    def get_queryset(self):
        branches_qs = Branch.objects.filter(milking=True)
        branches_scores_qs = BranchKPIs.objects.order_by('-date').defer(COW_COUNT)
        user = self.request.user
        self.kpis = user.user_selected_kpis.get_all_kpis_qs()
        query_set = Farm.objects.filter(account__account_users=user). \
            annotate(milking_cattle=Sum(Case(When(farm_branches__branch_scores__date=TWO_DAYS_AGO,
                                                  farm_branches__milking=True,
                                                  then='farm_branches__branch_scores__cow_count'))
                                        )
                     ). \
            select_related(RelatedNames.LOCATION). \
            prefetch_related(Prefetch(lookup=RelatedNames.FARM_SCORES,
                                      queryset=FarmKPIs.objects.filter(date__range=month_range).order_by('-date'),
                                      to_attr='farm_month_kpis'
                                      ),
                             Prefetch(lookup='farm_branches',
                                      queryset=branches_qs.prefetch_related(Prefetch(lookup=RelatedNames.BRANCH_SCORES,
                                                                                     queryset=branches_scores_qs,
                                                                                     to_attr='filtered_branches_scores'
                                                                                     )
                                                                            ).defer(RelatedNames.BRANCH_SCORES),
                                      ),
                             ).defer(SYSTEM_TYPE, SW_VERSION, UTC_OFFSET, LAST_SW_UPDATE,
                                     SYSTEM_KEY, DEALER_NAME, TIMEZONE)
        return query_set

    # @silk_profile()
    @extend_schema(summary="Farms Meta Data and KPIs", responses=FarmSerializerResponse)
    def list(self, request, *args, **kwargs):
        """
        Get all the farms associated with a the Authenticated User and those farms respective Branches and Groups IDs
        """
        query = self.get_queryset()
        farm_config, _ = FarmConfigurationsLayer.objects.get_or_create(id=1)
        farms = []
        for farm in query:
            farm_scores = farm.farm_month_kpis
            farm_stats = self._get_farm_stats(farm=farm, farm_config=farm_config, farm_scores=farm_scores)
            farm_data = self.serializer_class(farm, many=False).data
            farm_kpis = self._get_kpis(farm_kpis_list=farm_scores)
            farms.append({**farm_data, **farm_stats, KPIS: farm_kpis})
        return Response(farms)

    def _get_farm_stats(self, farm, farm_config, farm_scores):
        try:
            instance = farm_scores[0]  # try getting two days ago data
            aggregations = {COW_COUNT: instance.cow_count, ASSIGNED_TAG_COUNT: instance.assigned_tag_count}
        except (FarmKPIs.DoesNotExist, IndexError):  # doesn't exist, use latest
            aggregations = {COW_COUNT: 0, ASSIGNED_TAG_COUNT: 0}

        if aggregations[COW_COUNT] is None:
            aggregations[COW_COUNT] = 0
        if aggregations[ASSIGNED_TAG_COUNT] is None:
            aggregations[ASSIGNED_TAG_COUNT] = 0
        aggregations[FARM_SIZE] = self._get_farm_pin_size(aggregations[COW_COUNT], farm_config=farm_config)
        milking_cattle = farm.milking_cattle
        if milking_cattle is None or 0:
            try:
                milking_cattle = sum(
                    [branch.filtered_branches_scores[0].cow_count for branch in farm.farm_branches.all()])
            except IndexError:
                try:
                    milking_cattle = sum([branch.filtered_branches_scores[0].cow_count
                                          for branch in farm.farm_branches.all()])
                except Exception:
                    milking_cattle = 0
        aggregations[MILKING_CATTLE] = milking_cattle
        return aggregations

    def _get_farm_pin_size(self, cow_count, farm_config):
        if cow_count in farm_config.s_farm_size:
            return 1
        elif cow_count in farm_config.m_farm_size:
            return 2
        elif cow_count in farm_config.l_farm_size:
            return 3
        elif cow_count in farm_config.xl_farm_size:
            return 4
        else:
            return 2

    def _get_kpis(self, farm_kpis_list) -> Dict[str, int]:
        """
        compares every Farm KPI last 30 days average against the most recent value, if the recent value went,return 1,
        if it went down, return -1, if they the same or recent does not exist return 0
        """
        kpis = self.kpis
        import pandas as pd
        data = [model_to_dict(instance) for instance in farm_kpis_list]
        df = pd.DataFrame(data)
        try:
            latest_kpis = data[0]
        except IndexError:
            latest_kpis = {}
        if df.empty is True:
            data = {kpi.internal_name: {DATE: TWO_DAYS_AGO, SCORE: 0, TREND: 0, SCORE_TYPE: 0} for kpi in kpis}
        else:
            data = {kpi.internal_name: {DATE: latest_kpis.get(DATE, TWO_DAYS_AGO),
                                        SCORE: latest_kpis.get(kpi.internal_name, 0),
                                        TREND: trend(latest_kpis.get(kpi.internal_name, 0),
                                                     df[kpi.internal_name].mean()),
                                        SCORE_TYPE: score_type_from_kpi(value=latest_kpis.get(kpi.internal_name, 0),
                                                                        kpi=kpi)
                                        } for kpi in kpis}
        return data


class TilesView(ScrListViewSet):

    def get_queryset(self):
        user = self.request.user
        scores = FarmKPIs.objects.filter(farm__account__account_users=user).order_by(FARM, '-date').distinct(FARM)
        return scores, user

    @extend_schema(summary="User Tiles", responses=TilesResponse)
    def list(self, request, *args, **kwargs):
        query, user = self.get_queryset()
        # list the user's selected
        kpis = request.query_params.get(KPIS, None)

        account_kpis = user.user_selected_kpis.get_all_kpis_qs() if kpis is None \
            else KPI.objects.filter(bundle__bundles_by_account=user.account)

        data = {kpi.internal_name: self._scores_types_counter(kpi=kpi, data=query) for kpi in account_kpis}
        return Response(data)

    def _scores_types_counter(self, kpi, data):
        kpi_name = kpi.internal_name

        red_range = kpi.farm_level_red_threshold
        yellow_range = kpi.farm_level_yellow_threshold
        green_range = kpi.farm_level_green_threshold

        red = 0
        yellow = 0
        green = 0

        scores = [getattr(farm_data, kpi_name) for farm_data in data]
        scores = [score == 0 if score is None else score for score in scores]

        avg = int(mean(scores)) if len(scores) > 0 else 0

        for item in scores:
            if item in red_range:
                red += 1
            elif item in yellow_range:
                yellow += 1
            elif item in green_range:
                green += 1
            else:
                yellow += 1

        return {AVG_SCORE: avg, RED: red, YELLOW: yellow, GREEN: green}
