import csv
from typing import Dict, List

import pandas as pd
from django.http import HttpResponse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from common.base.exceptions import TableNotFoundError, TableDoesNotExistError, UserHasNoAccessToThisKPI
from common.consts import DATE, TABLE, THRESHOLD, NAME
from common.consts import POPULATION
from common.dates.consts import YESTERDAY
from common.dates.request_handler import request_dates_handler
from common.dates.utils import construct_dates_dict, clean_dates_in_dict


class TablesBuilder:
    """
    This class receives time frame in days, fields in a model and a query of that model, and creates the following:
        construct data for graphs either as list of tuples or dictionary
        it also adds export to csv capabilities
        it can chain tables together if we want to export two tables together and such...
    """

    def __init__(self, graphs: dict, days: int = 30, end_date=timezone.now().date(), dates_range=None):
        self.graphs = graphs
        self.days = days
        self.end_date = end_date
        self.tables_enum = dict(enumerate(tuple(self.graphs.keys()), start=1))
        self.dates_range = dates_range

    def construct_graphs(self, query, specific_graph: int = None, by_table_name=None, replace_name=None,
                         ignore_keys=False, thresholds=None, **modify_graph_return) -> dict:
        """
        this method will take the graphs attribute and will create the data dictionary for every graph specified there.
        :param by_table_name: specify a table name and not the enum representation of it
        :param thresholds: adds a threshold parameter to each dictionary of every date's data
        :param specific_graph: specify only one graph to return
        :param replace_name: adds a suffix for each field except date field
        :param ignore_keys: matches param in the construct_tables_data method
        :param query: the queryset of model to filter on
        :param modify_graph_return: should be graph_name = True, if True then returns a tuple instead
        """
        constructed_graphs = {}

        if specific_graph is not None or by_table_name is not None:
            if specific_graph is not None:
                graph_name = self.tables_enum[int(specific_graph)]
                fields = self.graphs[graph_name]
            if by_table_name is not None:
                graph_name = by_table_name
                fields = self.graphs[graph_name]

            threshold = thresholds[graph_name] if thresholds is not None else None
            as_tuple = modify_graph_return.get(graph_name, False)
            key_field = fields[0]
            fields = fields[1:]
            constructed_graphs[graph_name] = self._construct_table(*fields, query=query, as_key_field=key_field,
                                                                   as_tuple=as_tuple, ignore_keys=ignore_keys,
                                                                   replace_field_name=replace_name, threshold=threshold)
        else:
            for graph in self.graphs.items():
                as_tuple = modify_graph_return.get(graph[0], False)
                key_field = graph[1][0]

                threshold = thresholds[graph[0]] if thresholds is not None else None

                if len(graph[1]) == 1:
                    fields = list(graph[1][1])
                else:
                    fields = list(graph[1][1:])

                graph_data = self._construct_table(*fields, query=query, as_key_field=key_field, as_tuple=as_tuple,
                                                   ignore_keys=ignore_keys, replace_field_name=replace_name,
                                                   threshold=threshold)
                constructed_graphs.update({graph[0]: graph_data})

        return constructed_graphs

    def export_to_csv(self, query, table, chain_list: list = None, fields_names=None, farm_name=None, branch_name=None):
        """
        this method creates csv formatted version of one of the graphs in the site stats endpoint
        it receives the site id and table number
        the table number matches the numbering from the site stats tables response
        :param farm_name: adds the name to each row
        branch_name: adds the population name to each row (refers to any population model that exist, except farm)
        :param fields_names: custom headers names
        :param query: query to execute
        :param table: table number to export
        :param chain_list: list containing tables numbers (like the enum) to chain together to one table
        """
        if chain_list is not None:
            return self._chain_tables(query=query, chain_list=chain_list)
        else:
            table_to_return, fields, key_field = self.get_table(table, query)
            return self.construct_csv_return(table=table, table_to_return=table_to_return, fields_names=fields_names,
                                             farm_name=farm_name, branch_name=branch_name)

    def construct_csv_return(self, table_to_return, table=None, name=None, fields_names: tuple = None,
                             farm_name=None, branch_name=None, **kwargs):
        """
        given the dictionary builds a Dataframe, organizes it in csv comfortable format,
        and construct a Django response that outputs a CSV
        :param branch_name: adds the branch/group name to the columns
        :param farm_name: if not None adds to each row the farm's name
        :param fields_names: specify custom fields names
        :param table: specify table by id
        :param table_to_return: the returned data
        :param name: file name
        :param kwargs: adds additional constant to the csv
        :rtype django.http.HttpResponse
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' f"filename={table}.csv" if name is None \
            else 'attachment;' f"filename={name}.csv"
        data = table_to_return[table] if not isinstance(table_to_return, list) else table_to_return
        fields_names = fields_names if fields_names is not None else tuple(data[0].keys())
        if kwargs:
            fields_names += tuple(kwargs.keys())
        writer = csv.DictWriter(response, fieldnames=fields_names)
        writer.writeheader()

        for di in data:
            if kwargs:
                for col in kwargs:
                    di[col] = kwargs[col]
            if farm_name is not None:
                di[NAME] = farm_name
                di[POPULATION] = farm_name if branch_name is None else branch_name
            writer.writerow(di)
        return response

    def _load_to_df(self, table_to_return, key_field, fields, replace_field_name=None, rename: dict = None,
                    threshold=None):
        """
        :param threshold a threshold number to add to each dictionary that will be created
        load table_to_return into a pandas DF in order to organize and set the columns
        relation to the other values.
        """
        if isinstance(table_to_return, list):
            df = pd.DataFrame(table_to_return, columns=fields)

        else:
            if len(fields) > 1:
                for date in table_to_return:
                    try:
                        # if more then one field is specified, get those into a list,
                        # the dataframe will get the fields names directly
                        table_to_return[date] = tuple(table_to_return[date].values())
                    except AttributeError:
                        # handles 0 values more properly as the table to return
                        # can return 0 if no value was found in query
                        table_to_return[date] = [0 for i in range(len(fields))]
            pass
            df = pd.DataFrame.from_dict(table_to_return, orient='index', columns=fields)
            df[key_field] = tuple(table_to_return.keys())

        df.rename(rename, axis='columns', inplace=True) if rename is not None else df

        df.rename({field: replace_field_name for field in fields if field is not DATE},
                  axis='columns', inplace=True) if replace_field_name is not None else df

        if threshold is not None:
            df[THRESHOLD] = threshold
        else:
            pass
        # convert back to formatted dictionary and fill accidental null values
        table = df.fillna(0).to_dict(orient='records')
        return table

    def _construct_table(self, *fields, query, as_key_field, replace_field_name=None, as_tuple=False, ignore_keys=True,
                         rename: dict = None, threshold: int = None):
        """
        this method takes in a list of dictionaries (as created by Django's values method for example and returns
        an unpacked version of the values with 0 to fill missing dates values.

        :param rename: dictionary specifying if to rename the fields returning, keys should be original fields
                       and values as new names
        :param ignore_keys: if True, will reconstruct the return dictionary to contain with fields and values instead of
                            key field : value
        :param fields: specify X number of fields (Model Fields) to unpack as values,
               if specified leave as value field empty
               if number of fields is set to one returns an unpacked version of the dictionary
               where as_key_field : the given field
               if more then one series is used, constructs a nested dictionary
               where field name is key and corresponding values

        :param query: a query to list it's values
        :type query: django.db.models.QuerySet
        :param as_key_field: the query's field to use as the new dictionaries keys

        :param as_tuple: if True, returns only the values as a tuple, if false,
                         returns the dictionary along with the dates.

        :rtype tuple or dict
        """
        if len(fields) == 0:
            raise AttributeError('you need to specify at least one field')
        list_of_dicts = list(query.values(as_key_field, *fields))  # create the values list

        # unpack the dictionaries
        if len(fields) == 1:
            counts_dict = {di[as_key_field]: di[fields[0]] for di in list_of_dicts}
        else:
            counts_dict = {di[as_key_field]: {field: di[field] for field in fields} for di in list_of_dicts}

        # constructs a dictionary of last 30 dates with 0 as values
        dates_dict = construct_dates_dict(end_date=self.end_date, days=self.days)

        data = self._match_data_with_dates(counts_dict=counts_dict, dates_dict=dates_dict, as_tuple=as_tuple)

        return self._load_to_df(data, key_field=as_key_field, fields=fields, rename=rename,
                                replace_field_name=replace_field_name, threshold=threshold) \
            if ignore_keys else data

    def _match_data_with_dates(self, counts_dict, dates_dict, as_tuple):
        """
        given two dictionary, one with dates as keys and 0 as values, and one with real data, fill a new dictionary that
        replaces the 0 where the data is real
        :returns: tuple or dictionary
        """
        real_dates = tuple(counts_dict.keys())
        filled_dates = tuple(dates_dict.keys())

        for date in real_dates:
            if date in filled_dates:
                dates_dict[date] = counts_dict[date]  # match date with actual data

        if as_tuple is False:
            data = clean_dates_in_dict(dates_dict)
        else:
            data = tuple(dates_dict.values())
        return data

    def _get_fields(self, table):
        """
        returns the table's key field and values fields
        """
        if table not in self.graphs.keys():
            raise UserHasNoAccessToThisKPI

        graph_fields = self.graphs[table]  # get it's fields
        key_field = graph_fields[0]
        graph_fields.remove(graph_fields[0])
        fields = graph_fields
        return key_field, fields

    def get_table(self, table, query):
        """
        construct a table
        """
        key_field, fields = self._get_fields(table)
        table_to_return = self._construct_table(*fields, query=query, as_key_field=key_field)
        return table_to_return, fields, key_field

    def _chain_tables(self, chain_list, query):
        """
        creates and chains multiple tables together
        """
        main_key_field = None
        full_fields = []
        for table_num in chain_list:
            key_field, fields = self._get_fields(table_num)
            full_fields.extend(fields)
            main_key_field = key_field

        data = self._construct_table(*full_fields, query=query, as_key_field=main_key_field, ignore_keys=False)

        # retrieval number will extend the tables enum attribute
        table_enum = len(self.tables_enum.keys()) + 1
        table_name = " & ".join(list(full_fields) * len(full_fields))  # construct name out of fields names

        self.tables_enum.update({table_enum: table_name})  # update the enum with new chained table
        return self.construct_csv_return(table=table_enum, table_to_return=data)

    def reconstruct_for_comparison(self, as_exporter, dfs, name_field, file_name=None, thresholds=None):
        """
        reconstructs and merges graphs for comparing.
        we give it the constructed graph for each ID and it returns a dictionary like this:
        {id_x_score:40, id_y_score:50,date:10-10-2020} for every date
        """
        data = dict()

        cols = dfs[0].columns[1:-1].to_list()
        for col in cols:
            new_df = pd.DataFrame({DATE: dfs[0][DATE]})
            for df in dfs:
                if (df[cols[0]] == 0).all() is False:
                    dates_range = pd.date_range(start=df.date.min(), end=df.date.max())
                    df.set_index(DATE).reindex(dates_range).fillna(0).rename_axis(DATE).reset_index()
                else:
                    pass
                site_name = df[name_field].unique()[0]
                dropped = df.drop(name_field, axis='columns')
                new_df[site_name] = df[col]
                if as_exporter is False:
                    new_df[THRESHOLD] = thresholds[col]
                new_df.fillna(0, inplace=True)
            data[col] = new_df.to_dict('records')
            t_name = col
        return data if as_exporter is False else self.construct_csv_return(table_to_return=data,
                                                                           table=t_name,
                                                                           name=file_name,
                                                                           kpi=t_name)

    def request_handler(self, request, with_table=True, default_end_date=YESTERDAY):
        """
        this method receives the DRF request object and based on the passed parameters returns end date, dates range
        and days difference between end and start dates, if needed it will raise proper errors.
        it defaults to handle start and end date, along with quarter which will return data from start of quarter till
        yesterday, it can be overridden to address other fields as well.
        :param default_end_date: specify a default end date, can be none and it will default to YESTERDAY
        :type request: rest_framework.request.Request
        :type with_table: the regular builder doesnt have specify a table number in the request,
              so we we'll want to skip it
        """
        days, dates_range, end_date = request_dates_handler(request=request, default_end_date=default_end_date)
        if with_table:
            table_id = self.handle_table_id(request=request)
            return days, dates_range, end_date, table_id
        return days, dates_range, end_date

    def handle_table_id(self, request):
        try:
            table = int(request.query_params[TABLE][0])
            tables_range = list(range(len(self.tables_enum.keys()) + 1))
            # if requested table number does not exist
            if table not in tables_range:
                raise TableDoesNotExistError
            else:
                return table
        except MultiValueDictKeyError:
            raise TableNotFoundError  # if no table supplied raise error


def tables_builder(graphs: Dict[str, List[str]], days=None, end_date=None, dates_range=None):
    """
    this method receives a dictionary,
       keys should the desired graphs names.
       values should be the fields names used in every graph with the following order:
           first field is the the by series and the following fields will be the Data series, it can be unlimited.
    example:
       graphs = {'scores_over_last_30_days' : ['date','site_score','read_success'],
                 'movement_over_last_30_days':['date','entrances_on_site','exits_on_site']
                 }
    """
    return TablesBuilder(graphs, days=days, end_date=end_date, dates_range=dates_range)
