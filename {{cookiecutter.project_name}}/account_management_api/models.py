from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from rest_framework_api_key.permissions import BaseHasAPIKey

from common.consts import DATE
from common.dates.consts import TODAY


class UsageReports(models.Model):
    date = models.DateField(null=True, blank=True)
    raw_report = models.TextField(default='')
    month: int = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    zoura_import_status_url = models.URLField()
    successfully_sent: bool = models.BooleanField(default=False,
                                                  help_text="When we send the request, "
                                                            "if it wasn't successful, we'll try again day after")

    retry_failed = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'Monthly Usage Report'
        verbose_name_plural = 'Monthly Usage Reports'
        unique_together = ((DATE, 'zoura_import_status_url'),)

    def save(self, *args, **kwargs):
        self.date = TODAY
        super().save(*args, **kwargs)


class SalesForceApiKey(AbstractAPIKey):
    pass


class HasSalesForceApiKey(BaseHasAPIKey):
    model = SalesForceApiKey
