from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .api_views import (
	CotacoesDasAcoesModelViewSet
)

router = DefaultRouter()
router.register('cotacoes-das-acoes', CotacoesDasAcoesModelViewSet)

urlpatterns = [
	path('api/v1/', path(router.urls)),
]
