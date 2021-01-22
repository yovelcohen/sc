import os
import pickle as pkl

from google.api_core import retry
from google.cloud import storage
from google.oauth2 import service_account


class GCPBucketConnector(object):
    def __init__(self, project_name, bucket_name, CREDS_DICT):
        creds = service_account.Credentials.from_service_account_info(CREDS_DICT)
        storage_client = storage.Client(project=project_name, credentials=creds)
        self._bucket_name = bucket_name
        self._bucket_object = storage_client.get_bucket(self._bucket_name)

    def get_latest_file_in_folder(self, folder_path):
        relevant_blobs = self._bucket_object.list_blobs(prefix=folder_path)
        sorted_blobs = sorted(relevant_blobs, key=lambda x: x.time_created)
        latest_file_uploaded_path = sorted_blobs[-1].name
        return latest_file_uploaded_path

    @retry.Retry(deadline=210)
    def download_file(self, folder_path, file_name=None):
        file_path = os.path.join(folder_path, file_name) if file_name else self.get_latest_file_in_folder(folder_path)
        print("Downloading file from: {}".format(file_path))
        blob = self._bucket_object.blob(file_path)
        # Download the file to a destination
        file_obj = blob.download_to_file()
        return file_obj

    def download_pickle(self, folder_path, file_name=None):
        file_path = os.path.join(folder_path, file_name) if file_name else self.get_latest_file_in_folder(folder_path)
        print("Downloading file from: {}".format(file_path))
        blob = self._bucket_object.blob(file_path)
        # Download the file to a destination
        pkl_obj = blob.download_as_string()
        file_obj = pkl.loads(pkl_obj)
        return file_obj

    def upload_file(self, file_obj, dst_file_path):
        print("Uploading file to: {}".format(dst_file_path))
        blob = self._bucket_object.blob(dst_file_path)
        blob.upload_from_file(file_obj)

    @retry.Retry(deadline=210)
    def upload_pickle(self, pickle_obj, dst_file_path):
        blob = self._bucket_object.blob(dst_file_path)
        blob.upload_from_string(data=pickle_obj)

    def list_files_paths(self, folder):
        """
        returns dictionary of all the files in the folder with they're last update date
        """
        blobs = self._bucket_object.list_blobs(prefix=folder)
        return {blob.name: blob.updated for blob in blobs}
