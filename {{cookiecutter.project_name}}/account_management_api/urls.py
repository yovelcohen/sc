from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account_management_api.views import AccountsView
from common.consts import ACCOUNTS

router = DefaultRouter()
router.register(r'accounts', AccountsView, basename=ACCOUNTS)

urlpatterns = [path('', include(router.urls)), ]
