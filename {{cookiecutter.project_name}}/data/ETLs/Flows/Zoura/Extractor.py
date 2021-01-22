import pandas as pd

from api.models import FarmScores
from common.consts import (FARM__ACCOUNT, FARM__ACCOUNT__ID, FARM__NAME, ASSIGNED_TAG_COUNT,
                           FARM__ACCOUNT__BILLING_ID, DATE, FARM)
from common.dates.consts import TODAY
from data.ETLs.Base.BaseExtractor import BaseExtractor


class DataForBillingReportExtractor(BaseExtractor):
    def extract(self):
        CURRENT_YEAR = TODAY.year
        CURRENT_MONTH = TODAY.month
        PREV_MONTH = CURRENT_MONTH - 1
        account_ids = self.accounts.values_list('id', flat=True)
        query = FarmScores.objects.filter(farm__account__in=account_ids, date__month=PREV_MONTH, date__day=15,
                                          date__year=CURRENT_YEAR).select_related(FARM, FARM__ACCOUNT)
        if not query.exists():
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(tuple(query.values(FARM__ACCOUNT__ID, FARM__NAME, ASSIGNED_TAG_COUNT, DATE,
                                                 FARM__ACCOUNT__BILLING_ID)))
        return df
