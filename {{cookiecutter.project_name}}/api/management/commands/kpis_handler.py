from base.dates.consts import FROM_DATE, TWO_DAYS_AGO, END_DATE
from common.base_ald_command import BaseALDCommand
from data.ETLs.Factory.Flows import ETLFlows
from data.ETLs.Runner import ETLRunner


class Command(BaseALDCommand):

    def handle(self, *args, **options):
        token = self.token
        farms = self.get_all()
        start_date = options.pop(FROM_DATE, None)
        end_date = options.pop(END_DATE, None)

        start_date = TWO_DAYS_AGO if start_date is None else start_date
        end_date = TWO_DAYS_AGO if end_date is None else end_date

        ETLRunner(token=token, flow=ETLFlows.FARM_KPIS,
                  start_date=start_date, end_date=end_date, multiple_farms=farms).run_etl_flow()
        ETLRunner(token=token, flow=ETLFlows.BRANCHES_KPIS,
                  start_date=start_date, end_date=end_date, multiple_farms=farms).run_etl_flow()
        ETLRunner(token=token, flow=ETLFlows.GROUP_KPIS,
                  start_date=start_date, end_date=end_date, multiple_farms=farms).run_etl_flow()
