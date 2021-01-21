from datetime import timedelta

from django.utils import timezone
from pytz import all_timezones

from common.dates.utils import create_dates_range, get_first_day_of_the_quarter

ONE_DAY = timedelta(days=1)
TWO_DAYS = timedelta(days=2)
TODAY = timezone.now().date()
YESTERDAY = TODAY - ONE_DAY

ONE_YEAR_AGO = TODAY - timedelta(days=365)
TWO_YEARS_AGO = TODAY - timedelta(days=730)

month_range = create_dates_range(days=30)
five_days_range = create_dates_range(days=5)
seven_days_range = create_dates_range(days=7)
TWO_DAYS_AGO = TODAY - TWO_DAYS
month_from_yesterday = create_dates_range(days=30, date=YESTERDAY)
quarter_start_date = get_first_day_of_the_quarter(TODAY)

TIMEZONES_CHOICES = tuple(zip(all_timezones, all_timezones))

QUARTER = 'quarter'
USE = 'use'
START_DATE = 'start_date'
UTC = 'UTC'
FROM_DATE = 'from_date'
END_DATE = 'end_date'
FromDate = 'FromDate'
EndDate = 'EndDate'
