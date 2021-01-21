from common.base_ald_command import BaseALDCommand
from consumer_api.models import Account
from data.ETLs.Factory.Flows import ETLFlows
from data.ETLs.Runner import ETLRunner


class Command(BaseALDCommand):
    def handle(self, *args, **options):
        accounts = Account.objects.all()
        ETLRunner(accounts=accounts, token=None, flow=ETLFlows.ZOURA_BILLING)
