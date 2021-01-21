from base_scr.common.consts import SYSTEM_KEY
from common.base_ald_command import BaseALDCommand
from data.ETLs.Factory.Flows import ETLFlows
from data.ETLs.Runner import ETLRunner


class Command(BaseALDCommand):
    def add_arguments(self, parser):
        parser.add_argument(SYSTEM_KEY, type=str)

    def handle(self, *args, **options):
        system_key = options.pop(SYSTEM_KEY, None)
        if system_key is None:
            ETLRunner(farm=None, flow=ETLFlows.FARMS_META, token=self.token,
                      multiple_farms=self.get_all()).run_etl_flow()
        ETLRunner(farm=None, flow=ETLFlows.FARMS_META, token=self.token, system_key=system_key).run_etl_flow()
