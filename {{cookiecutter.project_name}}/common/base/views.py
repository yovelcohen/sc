from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import (UpdateModelMixin, CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class PermittedSwagger(SpectacularSwaggerView):
    """
    In order to override the default permissions class which makes the docs require authenticating before access
    """
    permission_classes = []


class PermittedReDoc(SpectacularRedocView):
    permission_classes = []


class BaseScrGenericViewSet(GenericViewSet):
    """
    Base Traceability Dashboard API View
    extends the built in Generic View Set to supply generic behaviour across the config
    every view should inherit this class or any of it's extensions
    """
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (IsAuthenticated,)
    serializer_class = NotImplementedError


class CreateViewScr(CreateModelMixin, BaseScrGenericViewSet):
    """
    A custom View which can only receive POST and PUT methods.
    """
    pass


class DestroyUpdateCreateViewScr(DestroyModelMixin,
                                 CreateModelMixin,
                                 UpdateModelMixin,
                                 BaseScrGenericViewSet):
    """
    A custom view which can only receive POST, PUT and Delete methods.
    """
    pass


class ListViewSetScr(ListModelMixin,
                     BaseScrGenericViewSet):
    """
    A custom View which can only receive get request.
    """

    pass


class BaseScrModelViewSet(CreateModelMixin,
                          RetrieveModelMixin,
                          UpdateModelMixin,
                          DestroyModelMixin,
                          ListModelMixin,
                          BaseScrGenericViewSet):
    """
    exactly the same behaviour as a the builtin Model View Set, expects it inherits the config's extended Generic View Set
    """
    pass


class ScrBaseScrView(BaseScrGenericViewSet):

    def get_queryset(self):
        raise NotImplementedError


class ScrListViewSet(ListViewSetScr, ScrBaseScrView):
    pass


class ScrCreateViewSet(CreateViewScr, UpdateModelMixin, ScrBaseScrView):
    pass


class ScrUpdateViewSet(UpdateModelMixin, ScrBaseScrView):
    pass


class ScrListUpdateViewSet(UpdateModelMixin, ListViewSetScr, ScrBaseScrView):
    pass


class ScrModelViewSet(BaseScrModelViewSet, ScrBaseScrView):
    pass


class ScrCreateUpdateViewSet(CreateModelMixin, UpdateModelMixin, ScrBaseScrView):
    pass
