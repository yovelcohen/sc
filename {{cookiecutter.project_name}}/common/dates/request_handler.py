from common.base.exceptions import DateError
from common.dates.consts import TODAY, END_DATE, START_DATE
from common.dates.utils import convert_str_to_date, create_dates_range


def request_dates_handler(request, default_end_date):
    start_date = request.query_params.get(START_DATE, None)
    end_date = request.query_params.get(END_DATE, None)

    end_date = default_end_date if end_date is None else end_date

    if start_date is None:
        days = 30
        dates_range = create_dates_range(date=end_date, days=days)

    else:
        end_date = convert_str_to_date(end_date)
        start_date = convert_str_to_date(start_date)

        if end_date > TODAY or start_date > TODAY:
            raise DateError
        else:
            dates_range = [start_date, end_date]
            days = end_date - start_date

    return days, dates_range, end_date
