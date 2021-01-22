from django.contrib.auth.hashers import check_password
from djoser import utils
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from common.base.exceptions import UserNotFound
from common.base.views import BaseGenericViewSet, ScrCreateUpdateViewSet
from common.consts import RelatedNames, EMAIL, PASSWORD, TOKEN, FIRST_NAME, LAST_NAME, LANGUAGE
from users.models import User


class TokenCreateView(BaseGenericViewSet):
    """
    Use this endpoint to authenticate user and receive they're token and data
    """

    serializer_class = TokenCreateSerializer
    permission_classes = ()

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        email = self.request.data[EMAIL]
        password = self.request.data[PASSWORD]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotFound
        if user:
            check_user_password = check_password(password=password, encoded=user.password)
            if check_user_password is True:
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    Token.objects.create(user=user)
                    token = Token.objects.get(user=user)
                data = {TOKEN: token.key, FIRST_NAME: user.first_name, LAST_NAME: user.last_name,
                        EMAIL: user.email, LANGUAGE: user.language}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                raise UserNotFound


class TokenDestroyView(BaseGenericViewSet):
    permission_classes = settings.PERMISSIONS.token_destroy

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(ScrCreateUpdateViewSet):
    """
    Overriding djoser's Users view
    """

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):

        if request.method == "GET":
            user = User.objects.filter(email=self.get_object()).prefetch_related(RelatedNames.AUTH_TOKEN)[
                0]
            data = {FIRST_NAME: user.first_name,
                    LAST_NAME: user.last_name,
                    EMAIL: user.email,
                    LANGUAGE: user.language,
                    TOKEN: user.auth_token.key}
            return Response(data=data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            user = self.request.user
            data = self.request.data
            User.objects.filter(email=user.email).update(**data)
            updated_user = User.objects.get(email=user.email)
            data = {FIRST_NAME: updated_user.first_name,
                    LAST_NAME: updated_user.last_name,
                    EMAIL: updated_user.email,
                    LANGUAGE: updated_user.language,
                    TOKEN: updated_user.auth_token.key}
            return Response(data)
