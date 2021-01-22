from django.conf.urls import url
from django.urls import include, path
from djoser.views import TokenDestroyView, UserViewSet, TokenCreateView
from rest_framework.routers import DefaultRouter

users = DefaultRouter()
users.register("users", UserViewSet, basename='users')

login = DefaultRouter()
login.register('token', TokenCreateView, basename='login')

urlpatterns = [
    path('', include(login.urls)),
    path('', include(users.urls)),
    url(r"^token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]
