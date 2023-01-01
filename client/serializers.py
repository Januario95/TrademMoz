from rest_framework import serializers

from .models import (
	CotacoesDasAcoes,
)

class CotacoesDasAcoesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CotacoesDasAcoes
		fields = '__all__'



