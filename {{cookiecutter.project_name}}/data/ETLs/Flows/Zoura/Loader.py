import requests

from account_management_api.models import UsageReports
from common.consts import AUTHORIZATION, FILE, ACCESS_TOKEN
from common.dates.consts import TODAY
from common.utils.utils import marker_wrapper_printer
from data.ETLs.Base.BaseLoader import BaseLoader
from data.Resources import URLs, get_zoura_auth_token


class ZouraBillingLoader(BaseLoader):
    CURRENT_YEAR = TODAY.year
    CURRENT_MONTH = TODAY.month
    PREV_MONTH = CURRENT_MONTH - 1

    def validate_data(self, status_code, failed):
        if failed is True:
            # this for now, later when PO decides on which logic to implement here, we'll change
            marker_wrapper_printer(f'sending report to zoura failed with code {status_code}, will try later')
            return False
        return True

    def load(self):
        report_name = f'Alderan_{self.CURRENT_YEAR}_{self.CURRENT_MONTH - 1}_usage_report.csv'
        self.transformed_data.to_csv(report_name, index=False, date_format='%m/%d/%Y')
        response_url, response_code, response_content, failed = self._send_usage_report_to_zoura(report_name)
        self.validate_data(status_code=response_code, failed=failed)
        self._save_account_usage_data_to_db(response_url=response_url, failed=failed, report_name=report_name)

    def _send_usage_report_to_zoura(self, report_name):
        """
        sends the file to zoura api and returns the request status url
        """
        payload = {}
        files = [(FILE, (report_name, open(report_name, 'rb'), 'text/csv'))]
        token = get_zoura_auth_token()[ACCESS_TOKEN]
        headers = {AUTHORIZATION: f'Bearer {token}'}

        response = requests.request("POST", url=URLs.ZOURA_SAND_BOX, headers=headers, data=payload, files=files)

        response_json = response.json()
        if response.status_code == 200:
            try:
                response_url = response_json['checkImportStatus']
                failed = True
            except KeyError:
                response_url = f'{response_json["reasons"][0]["message"]} with processId: {response_json["processId"]}'
                failed = False
        else:
            response_url = 'failed_request'
            failed = False
        marker_wrapper_printer(f'request response: \n response code: {response.status_code} \n {response_url}')
        return response_url, response.status_code, response.content, failed

    def _save_account_usage_data_to_db(self, response_url, failed, report_name):
        """
        creates a usage report object
        total tags count is a dictionary that aggregates every account tags count,
        response url is the zoura url to that request processing page
        """
        with open(report_name, 'rb') as csvfile:
            import csv
            parsed_file = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in parsed_file:
                stringed_data = ', '.join(row)
        url = f'{URLs.ZOURA_SAND_BOX}/{response_url}'
        UsageReports.objects.create(file=stringed_data,
                                    zoura_import_status_url=url,
                                    successfully_sent=failed)
        marker_wrapper_printer('saved usage report to DB')
