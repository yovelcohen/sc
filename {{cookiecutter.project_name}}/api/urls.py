from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.graphs import GraphsView
from api.views.tiles import TilesView

router = DefaultRouter()
router.register(r'tiles', TilesView, basename='tiles')
router.register(r'graphs', GraphsView, basename='graphs')

urlpatterns = [
    path('', include(router.urls)),
]
