from django.urls import path, include
from rest_framework.routers import DefaultRouter

from consumer_api.views.graphs import GraphsView
from consumer_api.views.views import TilesView, FarmsView

router = DefaultRouter()
router.register(r'farms', FarmsView, basename='farms')
router.register(r'tiles', TilesView, basename='tiles')
router.register(r'graphs', GraphsView, basename='graphs')

urlpatterns = [
    path('', include(router.urls)),
]
