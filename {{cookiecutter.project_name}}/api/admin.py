from django.contrib.admin import ModelAdmin, AdminSite
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from api.models import GeoLocation, Account
from common.consts import (USER, KEY, CREATED, FIRST_NAME, EMAIL, LAST_NAME, LANGUAGE, IS_ADMIN, IS_ACTIVE, ACCOUNT, ID,
                           NAME, HAS_EXPIRED, CONTRACT_EXPIRATION_DATE, ZOURA_BILLING_ID, ZOURA_SUBSCRIPTION_ID)
from common.utils.custom_admin import export_to_csv


class LocationAdmin(ModelAdmin):
    pass


class TokenAdmin(ModelAdmin):
    list_display = [USER, KEY, CREATED]


class UsersAdmin(ModelAdmin):
    fields = [EMAIL, FIRST_NAME, LAST_NAME, ACCOUNT, LANGUAGE, IS_ADMIN, IS_ACTIVE]
    list_display = fields


class AccountAdmin(ModelAdmin):
    fields = (ID, NAME, CONTRACT_EXPIRATION_DATE, ZOURA_BILLING_ID, ZOURA_SUBSCRIPTION_ID, HAS_EXPIRED)
    list_display = fields
    readonly_fields = (HAS_EXPIRED,)
    search_fields = (NAME, ID)


class ConsumerAdmin(AdminSite):
    site_header = f'{{cookiecutter.project_slug_name}} BackEnd Admin'
    site_title = f'Admin of the {{cookiecutter.project_slug_name}} Dashboard admin'


consumer_admin = ConsumerAdmin('consumer_admin')
consumer_admin.add_action(export_to_csv)

admins = {Token: TokenAdmin, get_user_model(): UsersAdmin,
          GeoLocation: LocationAdmin, Account: AccountAdmin
          }

for item in admins.items():
    consumer_admin.register(item[0], item[1])
