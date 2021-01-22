import uuid

import pandas as pd
import six
from google.cloud import bigquery
from google.oauth2 import service_account


class BigQueryConnector(object):
    def __init__(self, project_name, GCP_CREDS_DICT):
        creds = service_account.Credentials.from_service_account_info(GCP_CREDS_DICT)
        self._bq_client = bigquery.Client(project_name, credentials=creds)
        self._project_name = project_name

    def run_query(self, query):
        job_id = str(uuid.uuid4())
        print("Run query with job_id={}".format(job_id))
        query_job = self._bq_client.query(query, job_id=job_id)
        results = query_job.result().to_dataframe()
        return results

    def get_table_schema(self, dataset_id, table_id):
        return self.get_table(dataset_id, table_id).schema

    def get_table(self, dataset_id, table_id):
        table_name = '.'.join([self._project_name, dataset_id, table_id])
        table = self._bq_client.get_table(table_name)
        return table

    def insert_rows(self, rows_to_insert, dataset_id, table_id):
        table = self.get_table(dataset_id, table_id)
        errors = self._bq_client.insert_rows(table, rows_to_insert)  # API request
        if errors:
            print("Got errors while writing data to BigQuery. ", errors[0:min(10, len(errors))])
        return not errors

    def write_dataframe(self, dataset_id, table_id, dataframe):
        table = self.get_table(dataset_id, table_id)
        table_schema = table.schema
        df_columns = set(dataframe.columns)
        schema_mandatory_columns = {val.name for val in table_schema if not val.is_nullable}
        schema_optional_columns = {val.name for val in table_schema if val.is_nullable}

        if len(schema_mandatory_columns - df_columns) > 0:
            raise KeyError("Dataframe misses mandatory columns: {}".format(schema_mandatory_columns - df_columns))

        if len(schema_optional_columns - df_columns) > 0:
            dataframe = dataframe.copy(deep=False)
            for col_name in schema_optional_columns - df_columns:
                dataframe[col_name] = None

        for col_name in [val.name for val in table_schema if val.field_type == 'STRING']:
            if col_name in dataframe.columns:
                dataframe[col_name] = dataframe[col_name].astype(six.text_type)

        records = [{k: v for k, v in m.items() if pd.notnull(v)} for m in dataframe.to_dict(orient='rows')]

        # Fix datetime columns
        date_columns = [(val.name, val.field_type) for val in table_schema if
                        val.field_type in ('DATE', 'DATETIME', 'TIMESTAMP')]
        for col_name, col_type in date_columns:
            if col_type == 'DATE':
                for record in records:
                    record[col_name] = record[col_name].isoformat()
            else:
                for record in records:
                    record[col_name] = record[col_name].to_pydatetime().isoformat()

        errors = self._bq_client.insert_rows_json(table, records)
        if errors:
            print("Got errors while writing data to BigQuery. ", errors[0:min(10, len(errors))])
        return not errors
