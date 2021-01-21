from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account_management_api.views import AccountsView, FarmsView
from base_scr.common.consts import FARMS, ACCOUNTS

router = DefaultRouter()
router.register(r'accounts', AccountsView, basename=ACCOUNTS)
router.register(r'farms', FarmsView, basename=FARMS)

urlpatterns = [path('', include(router.urls)), ]
