import os
from typing import Type

from django.db.models import Model



class BaseLoader:
    def __init__(self, transformed_data, farm=None):
        self.transformed_data = transformed_data
        self.farm = farm

    def validate_data(self, *args, **kwargs):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def bulk_load_using_django_orm(self, model: Type[Model], ignore_conflicts=True):
        """
        uses django model to load the data to the DB
        """
        validated = self.validate_data()
        if validated is False:
            marker_wrapper_printer(f'failed to validate data was found for {model.__name__}')
            return None
        else:
            data = self.transformed_data.to_dict(orient='records')
            objs = [model(**item) for item in data]
            model.objects.bulk_create(objs, ignore_conflicts=ignore_conflicts)
            marker_wrapper_printer(f'uploaded {model.__name__} data to DB successfully')
            return objs

    def load_dataframe_to_db_directly(self):
        """
        loads a pandas dataframe directly to SQL server, faster than the Django ORM, so useful in large datasets.
        """
        raise NotImplemented

    def upload_files_to_static_storage(self, connection_handler, folder, file_name):
        """
        handles uploading data to static files storage (GCP storage, AWS S3...)
        """
        path = os.path.join(folder, file_name)
        connection_handler.upload_file(path, self.transformed_data)
        return self.transformed_data
