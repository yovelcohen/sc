from api.models import Account
from common.base.command import ScrBaseCommand
from data.ETLs.Factory.Flows import ETLFlows
from data.ETLs.Runner import ETLRunner


class Command(ScrBaseCommand):
    def get_all(self):
        return Account.objects.all()

    def handle(self, *args, **options):
        accounts = self.get_all()
        ETLRunner(accounts=accounts, token=None, flow=ETLFlows.ZOURA_BILLING)
