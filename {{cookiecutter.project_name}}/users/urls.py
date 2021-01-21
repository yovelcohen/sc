from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import TokenCreateView, CustomUserViewSet, TokenDestroyView

users = DefaultRouter()
users.register("users", CustomUserViewSet, basename='users')

login = DefaultRouter()
login.register('token', TokenCreateView, basename='login')

urlpatterns = [
    path('', include(login.urls)),
    path('', include(users.urls)),
    url(r"^token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]
