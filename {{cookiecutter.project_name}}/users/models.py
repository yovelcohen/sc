from django.db import models

from api.models import Account
from common.base.models import ScrUserModel
from common.consts import RelatedNames


class User(ScrUserModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name=RelatedNames.ACCOUNT_USERS,
                                blank=True, null=True)

    class Meta:
        db_table = 'users'
