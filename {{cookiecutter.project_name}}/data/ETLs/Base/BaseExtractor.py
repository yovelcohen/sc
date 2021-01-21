from datetime import datetime

import requests

from common.consts import SystemKey
from common.dates.consts import FromDate, EndDate
from common.dates.utils import convert_datetime_to_unix


class BaseExtractor:
    def __init__(self, token=None, start_date=None, end_date=None, farm=None, accounts=None):
        self.farm = farm
        self._token = token
        self.start_date = convert_datetime_to_unix(start_date) if start_date is not None else start_date
        self.end_date = convert_datetime_to_unix(end_date) if end_date is not None else end_date
        self.accounts = accounts

    def extract(self):
        raise NotImplementedError

    def convert_time_stamp(self, date):
        string_date = date[:10]
        f_date = datetime.strptime(string_date, '%Y-%m-%d').date()
        return f_date

    def construct_query_params(self):
        if self.start_date is None and self.end_date is None:
            return {SystemKey: self.farm.system_key}
        elif self.start_date is not None and self.end_date is None:
            return {SystemKey: self.farm.system_key, FromDate: self.start_date}
        else:
            if self.farm is not None:
                return {SystemKey: self.farm.system_key, FromDate: self.start_date, EndDate: self.end_date}
            else:
                return {FromDate: self.start_date, EndDate: self.end_date}

    def _dp_headers(self):
        headers = {'Authorization': f'Bearer {self._token}'}
        return headers

    def get_data_from_adp(self, url):
        res = requests.get(url=url, params=self.construct_query_params(), headers=self._dp_headers())
        return res.json()
