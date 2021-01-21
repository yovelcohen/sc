from django.contrib.admin import ModelAdmin

from common.consts import USER, KEY, CREATED, FIRST_NAME, EMAIL, LAST_NAME, LANGUAGE, IS_ADMIN, IS_ACTIVE, ACCOUNT, ID, \
    NAME, HAS_EXPIRED, CONTRACT_EXPIRATION_DATE, ZOURA_BILLING_ID, ZOURA_SUBSCRIPTION_ID


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
