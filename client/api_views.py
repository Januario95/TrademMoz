from rest_framework.viewsets import ModelViewSet

from .models import (
	CotacoesDasAcoes
)

from .serializers import (
	CotacoesDasAcoesSerializer,
)

class CotacoesDasAcoesModelViewSet(ModelViewSet):
	queryset = CotacoesDasAcoes
	serializer_class = CotacoesDasAcoesSerializer


