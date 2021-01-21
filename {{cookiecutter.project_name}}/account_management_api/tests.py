from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from model_mommy import mommy

from base.consts import USER
from common.test_params import TEST_ACCOUNTS, create_farms
from consumer_api.models import Account
from users.models import User


class TestSendingUsageDataToZoura(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(email='demo1@email.com', password='top_secret1')
        user_2 = User.objects.create_user(email='demo2@email.com', password='top_secret2')
        TEST_ACCOUNTS[0].update({USER: user_1})
        TEST_ACCOUNTS[1].update({USER: user_2})
        self.accounts = Account.objects.bulk_create([Account(**account) for account in TEST_ACCOUNTS])
        farms1, farms2 = create_farms()
        for farm in farms1:
            farm.account = self.accounts[0]
        for farm in farms2:
            farm.account = self.accounts[1]
        farms = [*farms1, *farms2]
        for farm in farms:
            mommy.make('api.FarmKPIs', farm=farm)

    def test_creating_and_sending_usage_reports(self):
        out = StringIO()
        call_command(
            'send_usage_data',
            stdout=out
        )
        self.assertIn(
            200,
            out.getvalue()
        )
