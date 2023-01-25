from rest_framework import serializers

from .models import (
	CotacoesDasAcoes, Company
)


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'
		

class CotacoesDasAcoesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CotacoesDasAcoes
		fields = '__all__'



