from datetime import date

from django.db import models

from common.base.exceptions import ContractExpirationDateError
from common.base.models import BaseGeoLocation
from common.dates.consts import TODAY


class GeoLocation(BaseGeoLocation):
    pass


class Account(models.Model):
    id: str = models.CharField(max_length=100, primary_key=True, help_text='Account ID')
    name: str = models.CharField(max_length=255, default='default_account')
    zoura_subscription_id: str = models.CharField(max_length=100, null=True, blank=True)
    zoura_billing_account_id: str = models.CharField(max_length=100, null=True, blank=True)
    contract_expiration_date: date = models.DateField(null=True, blank=True)

    show_logo = models.BooleanField(default=False)
    logo_name = models.CharField(max_length=100, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.contract_expiration_date is not None:
            if self.contract_expiration_date < TODAY:
                raise ContractExpirationDateError
            pass
        pass
        super().save(*args, **kwargs)
