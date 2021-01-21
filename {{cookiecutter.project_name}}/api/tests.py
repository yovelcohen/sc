import django
from django.test import TestCase

django.setup()  # for pycharm debugging

from consumer_api.models import Farm, Account, FarmKPIs, Branch


class SignalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(id='a1', name='test')

    def test_farm_creation_signal(self):
        farm = Farm(id='77616', system_key='EU4862054', name="GAEC Bigot",
                    active=True, account=self.account)
        farm.save()
        # check that KPIs Are getting in from last two years
        self.assertTrue(FarmKPIs.objects.filter(farm=farm).exists())
        # check getting branches
        self.assertTrue(Branch.objects.filter(farm=farm).exists())
        # check that we got the farm's metadata from ADP
        self.assertEquals(farm.farm_type, 'DairyFarm')
        self.assertEquals(farm.farm_housing, 'SemiGrazing')
