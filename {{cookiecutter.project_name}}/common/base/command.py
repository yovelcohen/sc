from datetime import timedelta

from django.core.management import BaseCommand

from common.dates.consts import TODAY, END_DATE, FROM_DATE
from common.dates.utils import convert_str_to_date
from common.consts import FARM


class ScrBaseCommand(BaseCommand):

    def handle(self, *args, **options):
        raise NotImplementedError

    def __doc__(self):
        return self.help

    def get_all(self):
        """
        :returns all of the Base level model (farm/site)
        """
        raise NotImplementedError

    def add_arguments(self, parser):
        parser.add_argument(FROM_DATE, type=str, nargs='?')
        parser.add_argument(END_DATE, type=str, nargs='?')
        parser.add_argument(FARM, type=str, nargs='?',)

    def handle_dates(self, default, start_date, end_date=None):
        """
        checks if a date was given in the args, if so, creates a list of dates from that day to today,
        if that date is None, returns a list with only today in it
        :param start_date: date to end list range with
        :param end_date: date to start list range with
        :param default: if both dates are None, choose a date to populate list with
        :rtype list
        """
        if end_date:
            end_date = convert_str_to_date(end_date)
        if start_date:
            start_date = convert_str_to_date(start_date)
        dates = self._handle_dates(default=default, start_date=start_date, end_date=end_date)
        return dates

    def _handle_dates(self, default, start_date, end_date=None):
        if end_date is not None and start_date is not None:
            days_diff = end_date - start_date
            date_list = [start_date + timedelta(days=x) for x in range(abs(days_diff.days) + 1)]
            return date_list

        elif start_date is not None and end_date is None:
            days_diff = abs((TODAY - start_date).days)
            dates = [start_date + timedelta(days=x) for x in range(days_diff)]

        elif end_date is not None and start_date is None:
            raise AttributeError("end date can't be specified without start date")

        else:
            dates = [default, ]  # if no date is specified, run on yesterday
        return dates
