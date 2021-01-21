"""
This is an example utilization of the ETLs
This example if from the Multi Farm Dashboard config
this signal receives every farm object that's created (it was created via account management api)
and immediately gets two years worth of data about the farm, it's additional meta data
and data about it's branches and groups, which would make available in the config in less than two minuets after it was
created in Sales Force.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Farm
from common.consts import ACCESS_TOKEN
from common.dates.consts import TWO_YEARS_AGO, TWO_DAYS_AGO
from data.ETLs.Factory.Flows import ETLFlows
from data.ETLs.Runner import ETLRunner
from data.Resources import get_data_platform_auth_token


@receiver(post_save, sender=Farm)
def get_farm_historic_kpis(sender, instance, created, **kwargs):
    token = get_data_platform_auth_token()[ACCESS_TOKEN]
    if created:
        # farm's meta data
        ETLRunner(flow=ETLFlows.FARMS_META, token=token, farm=instance).run_etl_flow()
        # last two years of farm kpis
        ETLRunner(farm=instance, token=token, flow=ETLFlows.FARM_KPIS,
                  start_date=TWO_YEARS_AGO, end_date=TWO_DAYS_AGO).run_etl_flow()
        # last two years of farm's branches kpis
        ETLRunner(farm=instance, token=token, flow=ETLFlows.BRANCHES_KPIS,
                  start_date=TWO_YEARS_AGO, end_date=TWO_DAYS_AGO).run_etl_flow()
        # last two years of farm's groups kpis
        ETLRunner(farm=instance, token=token, flow=ETLFlows.GROUP_KPIS,
                  start_date=TWO_YEARS_AGO, end_date=TWO_DAYS_AGO).run_etl_flow()
