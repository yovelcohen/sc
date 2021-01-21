from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import (UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class PermittedSwagger(SpectacularSwaggerView):
    """
    In order to override the default permissions class which makes the docs require authenticating before access
    """
    permission_classes = []


class PermittedReDoc(SpectacularRedocView):
    permission_classes = []


class BaseGenericViewSet(GenericViewSet):
    """
    Base Traceability Dashboard API View
    extends the built in Generic View Set to supply generic behaviour across the config
    every view should inherit this class or any of it's extensions
    """
    authentication_classes = [TokenAuthentication, ]
    permissions_classes = [IsAuthenticated, ]
    serializer_class = NotImplementedError


class CreateView(CreateModelMixin, BaseGenericViewSet):
    """
    A custom View which can only receive POST and PUT methods.
    """
    pass


class DestroyUpdateCreateView(DestroyModelMixin,
                              CreateModelMixin,
                              UpdateModelMixin,
                              BaseGenericViewSet):
    """
    A custom view which can only receive POST, PUT and Delete methods.
    """
    pass


class ListViewSet(ListModelMixin,
                  BaseGenericViewSet):
    """
    A custom View which can only receive get request.
    """

    pass


class BaseModelViewSet(CreateModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       ListModelMixin,
                       BaseGenericViewSet):
    """
    exactly the same behaviour as a the builtin Model View Set, expects it inherits the config's extended Generic View Set
    """
    pass


class ScrBaseView(BaseGenericViewSet):

    def get_queryset(self):
        raise NotImplementedError


class ScrListViewSet(ListViewSet, ScrBaseView):
    pass


class ScrCreateViewSet(CreateView, UpdateModelMixin, ScrBaseView):
    pass


class ScrUpdateViewSet(UpdateModelMixin, ScrBaseView):
    pass


class ScrListUpdateViewSet(UpdateModelMixin, ListViewSet, ScrBaseView):
    pass


class ScrModelViewSet(BaseModelViewSet, ScrBaseView):
    pass


class ScrCreateUpdateViewSet(CreateModelMixin, UpdateModelMixin, ScrBaseView):
    pass
