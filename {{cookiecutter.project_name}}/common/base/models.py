"""
BASE SCR MODELS
all models are abstract and should be inherited, as we don't want to direct access to this file
"""
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from common.base.managers import SiteUserManager
from common.consts import COUNTRIES_CHOICES, EMAIL, EMAIL_ADDRESS, EN
from common.consts import RelatedNames

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'."
                                     " Up to 15 digits allowed.")


class BaseGeoLocation(models.Model):
    """
    Basic Location Model
    """
    latitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    street = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=30, choices=COUNTRIES_CHOICES, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.latitude}/{self.longitude}' if \
            all([self.street, self.country, self.city]) is None else f'{self.street}, {self.city}, {self.country}'

    def get_lat(self):
        return self.latitude or 0

    def get_long(self):
        return self.longitude or 0


class ScrBaseSiteModel(models.Model):
    """
    represents the highest level in the config, usually named farm or site
    """
    id = models.CharField(max_length=20, primary_key=True, verbose_name='Farm Id')
    name = models.CharField(max_length=255, verbose_name='Farm Name')
    location = models.ForeignKey('GeoLocation', on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name=RelatedNames.LOCATION)
    active = models.BooleanField(default=True)
    admin_email = models.EmailField()
    admin_phone = models.CharField(validators=[phone_regex], max_length=255, blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    def get_site_location(self):
        return str(self.location)

    def __str__(self):
        return self.name


class ScrBaseGroupModel(models.Model):
    """
    all applications have at the highest level (not including users/accounts) a Site or a Farm
    in Rivendell and Alderan those has lower levels of grouping, this is a Base model for them
    """

    name = models.CharField(max_length=100)
    milking: bool = models.BooleanField()

    objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def unique_error_message(self, model_class, unique_check, **kwargs):
        error = super().unique_error_message(model_class, unique_check)
        if len(unique_check) != 1:  # Intercept the unique_together error
            error.message = f'a {self.__class__.__name__} named: {self.name} is already on {self.site.name} '
        return error

    def site(self):  # prevents admin conflicts
        return self.site


class BaseScrScores(models.Model):
    """
    Base SCR Scores Model, usually applies at least at site/farm level, but can also be extended to lower level
    defines a meta and date field.
    also, since we have coloring based range system in few apps, serves an helpful utils to
    validate score type Base on ranges provided
    """
    date = models.DateField(default=now)
    cow_count = models.SmallIntegerField(default=0)
    objects = models.Manager()

    class Meta:
        ordering = ['-date']
        abstract = True


class ScrUserModel(AbstractUser):
    """
    Base User Model, uses email instead of user name to login
    """
    username = None
    email = models.EmailField(_(EMAIL_ADDRESS), unique=True)

    USERNAME_FIELD = EMAIL
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    language = models.CharField(max_length=7, choices=LANGUAGES, default=EN)

    objects = SiteUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        abstract = True

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.email
