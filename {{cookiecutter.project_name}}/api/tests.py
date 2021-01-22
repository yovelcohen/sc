import django
from django.test import TestCase

from api.models import Account

django.setup()  # for pycharm debugging


class SignalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(id='a1', name='test')

    def test_main_entity_creation_signal(self):
        """
        test that after the entity was created on SF and ADP we fetch it's data successfully
        """
        raise NotImplementedError
