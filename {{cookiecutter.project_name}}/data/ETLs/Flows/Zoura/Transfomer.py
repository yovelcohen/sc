from calendar import monthrange
from datetime import date

import numpy as np
import pandas as pd

from common.consts import (DATE, QTY, TAG, UOM, STARTDATE, ENDDATE, COSTUMERID, CHARGE_ID, DESCRIPTION, SITEID,
                           WORKFLOWRUNNUMBER, EXTERNALRECORDID, EXTERNALBATCHID)
from common.consts import (FARM__ACCOUNT__ID, FARM__ACCOUNT__BILLING_ID, SUBSCRIPTION_ID,
                           ACCOUNT_ID, FARMNAME, ASSIGNED_TAG_COUNT, FARM__NAME)
from common.dates.consts import TODAY
from data.ETLs.Base.BaseTransformer import BaseTransformer


class BillingDataTransformer(BaseTransformer):

    def transform(self):
        CURRENT_YEAR = TODAY.year
        CURRENT_MONTH = TODAY.month
        PREV_MONTH = CURRENT_MONTH - 1
        df: pd.DataFrame = self.data
        df.drop(columns=[DATE], inplace=True)
        df.rename({FARM__ACCOUNT__ID: ACCOUNT_ID.upper(), FARM__NAME: FARMNAME, ASSIGNED_TAG_COUNT: QTY,
                   FARM__ACCOUNT__BILLING_ID: SUBSCRIPTION_ID}, axis=1, inplace=True)

        # Unit of measure and dates columns
        df[UOM] = TAG
        prev_month_ending_day = monthrange(CURRENT_YEAR, PREV_MONTH)[1]  # get end day of previous month
        df[STARTDATE] = date(year=CURRENT_YEAR, month=PREV_MONTH, day=1)
        df[ENDDATE] = date(year=CURRENT_YEAR, month=PREV_MONTH, day=prev_month_ending_day)

        df[COSTUMERID] = 1

        # Zoura's demands the csv to be in this format, so we need to add this empty columns
        df[CHARGE_ID], df[DESCRIPTION], df[SITEID], df[WORKFLOWRUNNUMBER], df[EXTERNALRECORDID], \
        df[EXTERNALBATCHID] = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

        df[STARTDATE] = df[STARTDATE].apply(lambda x: x.strftime('%m/%d/%Y'))
        df[ENDDATE] = df[ENDDATE].apply(lambda x: x.strftime('%m/%d/%Y'))
        # if not applied the format is ruined when exported to csv
        df[STARTDATE] = df[STARTDATE].apply(str)
        df[ENDDATE] = df[ENDDATE].apply(str)
        return df
