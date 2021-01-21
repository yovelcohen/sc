from calendar import monthrange
from datetime import date

import numpy as np
import pandas as pd
import requests
from django.db.models import Sum

from account_management_api.models import UsageReports
from base.consts import (DATE, ENDDATE, STARTDATE, UOM, TAG, QTY, CHARGE_ID, DESCRIPTION, SITEID, WORKFLOWRUNNUMBER,
                         EXTERNALRECORDID, EXTERNALBATCHID, COSTUMERID)
from base_scr.common.consts import FARM, ACCOUNT_ID
from base_scr.data_platform_handler.utils import ZOURA
from common.base_ald_command import BaseALDCommand
from common.consts import (FARM__ACCOUNT, ASSIGNED_TAG_COUNT, THIRD_PARTY_URLS, FARM__NAME,
                           SUBSCRIPTION_ID, AUTHORIZATION, ZOURA_SAND_BOX,
                           FARMNAME, FARM__ACCOUNT__BILLING_ID, FILE, FARM__ACCOUNT__ID)
from common.utils import get_all_accounts, marker_wrapper_printer
from consumer_api.models import FarmKPIs, Farm


class Command(BaseALDCommand):
    help = "This command runs every month on the 15th and sends billing information about every farm usage. " \
           "Zoura expects a CSV file, so we need to generate the report for every account," \
           "unify those into a single csv file and send the request"

    token_type = ZOURA

    def get_all(self):
        return get_all_accounts()

    def handle(self, *args, **options):
        accounts = self.get_all()
        final_monthly_usage_report = pd.concat([self._construct_usage_data_csv(account) for account in accounts])

        final_monthly_usage_report[STARTDATE] = final_monthly_usage_report[STARTDATE].apply(
            lambda x: x.strftime('%m/%d/%Y'))
        final_monthly_usage_report[ENDDATE] = final_monthly_usage_report[ENDDATE].apply(
            lambda x: x.strftime('%m/%d/%Y'))

        final_monthly_usage_report[STARTDATE] = final_monthly_usage_report[STARTDATE].apply(str)
        final_monthly_usage_report[ENDDATE] = final_monthly_usage_report[ENDDATE].apply(str)

        # export it to csv file
        report_name = f'Alderan_{self.CURRENT_YEAR}_{self.CURRENT_MONTH - 1}_usage_report.csv'
        final_monthly_usage_report.to_csv(report_name, index=False, date_format='%m/%d/%Y')

        response_url, response_code, response_content, failed = self._send_usage_report_to_zoura(report_name)
        self._save_account_usage_data_to_db(final_monthly_usage_report, response_url, failed)

    def _construct_usage_data_csv(self, account):
        previous_month = self.CURRENT_MONTH - 1

        # filter and list all usages of farms under the given account
        query = FarmKPIs.objects.filter(farm__account=account, date__month=previous_month, date__day=15,
                                        date__year=self.CURRENT_YEAR).select_related(FARM, FARM__ACCOUNT)

        if not query.exists():
            return pd.DataFrame()
        else:
            self._save_farms_usage_data_to_db(account, query)

            # load it to DataFrame
            df = pd.DataFrame(tuple(query.values(FARM__ACCOUNT__ID, FARM__NAME, ASSIGNED_TAG_COUNT, DATE,
                                                 FARM__ACCOUNT__BILLING_ID)))

            df.drop(columns=[DATE], inplace=True)
            df.rename({FARM__ACCOUNT__ID: ACCOUNT_ID.upper(), FARM__NAME: FARMNAME, ASSIGNED_TAG_COUNT: QTY,
                       FARM__ACCOUNT__BILLING_ID: SUBSCRIPTION_ID}, axis=1, inplace=True)

            # Unit of measure and dates columns
            df[UOM] = TAG
            prev_month_ending_day = monthrange(self.CURRENT_YEAR, previous_month)[1]  # get end day of previous month
            df[STARTDATE] = date(year=self.CURRENT_YEAR, month=previous_month, day=1)
            df[ENDDATE] = date(year=self.CURRENT_YEAR, month=previous_month, day=prev_month_ending_day)

            df[COSTUMERID] = 1

            # Zoura's demands the csv to be in this format, so we need to add this empty columns
            df[CHARGE_ID], df[DESCRIPTION], df[SITEID], df[WORKFLOWRUNNUMBER], df[EXTERNALRECORDID], \
            df[EXTERNALBATCHID] = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

            return df

    # @retry_requests_decorator
    def _send_usage_report_to_zoura(self, report_name):
        """
        sends the file to zoura api and returns the request status url
        """
        payload = {}
        files = [(FILE, (report_name, open(report_name, 'rb'), 'text/csv'))]
        headers = {AUTHORIZATION: f'Bearer {self.token}'}

        response = requests.request("POST", url=THIRD_PARTY_URLS[ZOURA_SAND_BOX], headers=headers, data=payload,
                                    files=files)

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

    def _save_account_usage_data_to_db(self, final_df: pd.DataFrame, response_url, failed):
        """
        creates a usage report object
        total tags count is a dictionary that aggregates every account tags count,
        response url is the zoura url to that request
        """
        data = final_df.to_dict(orient='records')
        UsageReports.objects.create(file=data,
                                    zoura_import_status_url=response_url,
                                    successfully_sent=failed,
                                    month=self.CURRENT_MONTH - 1, year=self.CURRENT_YEAR)
        marker_wrapper_printer('saved usage report to DB')

    def _save_farms_usage_data_to_db(self, account, query):
        farms = Farm.objects.filter(account=account)
        farms_data = [FarmMonthlyUsage(farm=farm,
                                       tags_count=query.filter(farm=farm).
                                       aggregate(total_usage=Sum(ASSIGNED_TAG_COUNT))['total_usage'] or 0,
                                       month=self.CURRENT_MONTH - 1,
                                       year=self.CURRENT_YEAR) for farm in farms]
        FarmMonthlyUsage.objects.bulk_create(farms_data)
