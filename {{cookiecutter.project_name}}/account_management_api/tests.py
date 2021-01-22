from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from api.models import Account


class TestSendingUsageDataToZoura(TestCase):
    def setUp(self):
        User = get_user_model()
        user_1 = User.objects.create_user(email='demo1@email.com', password='top_secret1')
        user_2 = User.objects.create_user(email='demo2@email.com', password='top_secret2')
        TEST_ACCOUNTS = []
        self.accounts = Account.objects.bulk_create([Account(**account) for account in TEST_ACCOUNTS])

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
