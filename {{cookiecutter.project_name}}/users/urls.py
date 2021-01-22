from django.conf.urls import url
from django.urls import include, path, re_path
from djoser.views import TokenDestroyView, UserViewSet, TokenCreateView
from rest_framework.routers import DefaultRouter

users = DefaultRouter()
users.register("users", UserViewSet, basename='users')

urlpatterns = [
    re_path(r"^token/login/", TokenCreateView.as_view(), name="login"),
    path('', include(users.urls)),
    url(r"^token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]
