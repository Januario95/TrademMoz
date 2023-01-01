from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta


class Company(models.Model):
	name = models.CharField(
		max_length=125, default='CDM',
		unique=True)

	def __str__(self):
		return f'{self.name}'

	class Meta:
		ordering = ('id',)
		verbose_name = 'Company'
		verbose_name_plural = 'Companies'

class CotacoesDasAcoes(models.Model):
	date = models.DateField(blank=True)
	# nome_da_empresa = models.CharField(max_length=150)
	nome_da_empresa = models.ForeignKey(
		to=Company, on_delete=models.CASCADE)
	preco_da_acao = models.DecimalField(
		max_digits=20, decimal_places=2,
		default=0)

	def serialize(self):
		data = {
			'date': self.date,
			'nome_da_empresa': self.nome_da_empresa.name,
			'preco_da_acao': self.preco_da_acao
		}
		return data

	class Meta:
		verbose_name = 'Cotacao Da Acao'
		verbose_name_plural = 'Cotacoes Das Acoes'

	def __str__(self):
		return f'{self.nome_da_empresa} - {self.date} - {self.preco_da_acao}'

	def Variacao_Semestral(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=180),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 2)
			return result
		except Exception as e:
			print(e)
			return None

	def Variacao_Mensal(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=30),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 2)
			return result
		except Exception as e:
			print(e)
			return None

	def Variacao_Semanal(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=7),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 2)
			return result
		except Exception as e:
			print(e)
			return None

	def Variacao_Diaria(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=1),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 2)
			return result
		except Exception as e:
			print(e)
			return None

	def EV(self):
		try:
			balanco = Balanco.objects.get(ano=self.date.year-1)
			divida_liquida = TableDeDivida.objects.get(balanco=balanco).divida_liquida()
			Valor_Do_Mercado = self.Valor_Do_Mercado()
			return divida_liquida + Valor_Do_Mercado
		except Exception as e:
			print(e)
			return None

	def Valor_Do_Mercado(self):
		try:
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.date.year-1).numero_medio_ponderado_de_acoes
			return self.preco_da_acao * numero_medio_ponderado_de_acoes
		except Exception as e:
			print(e)
			return None


class MetricasPorAccao(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)
	nome_da_empresa = models.CharField(
		max_length=150, blank=True,
		default='CDM')

	class Meta:
		ordering = ('ano',)

	def EV_EBITDA(self):
		return None

	def EV_EBIT(self):
		return None

	def P_Capital_De_Giro_Liquido(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		Capital_de_Giro_Liquido = self.Capital_de_Giro_Liquido()
		try:
			date = round(date.last().preco_da_acao, 2)
			return round(date / Capital_de_Giro_Liquido, 2)
		except Exception as e:
			# print(e)
			return None

	def P_Capital_De_Giro(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		Capital_de_Giro = self.Capital_de_Giro()
		try:
			date = round(date.last().preco_da_acao, 2)
			return round(date / Capital_de_Giro, 2)
		except Exception as e:
			# print(e)
			return None

	def PSR(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		Vendas_Liquidas = self.Vendas_Liquidas()
		try:
			date = round(date.last().preco_da_acao, 2)
			return round(date / Vendas_Liquidas, 2)
		except Exception as e:
			# print(e)
			return None

	def Dividend_Yield(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		dividendo_por_acao = DemonstracaoDeResultados.objects.get(ano=year).dividendo_por_acao()
		try:
			date = round(date.last().preco_da_acao, 2)
			return round((dividendo_por_acao / date) * 100, 2)
		except Exception as e:
			# print(e)
			return None

	def EBIT_ACTOVOS(self):
		EBIT_ = self.EBIT_()
		Activos = self.Activos()
		DemonstracaoDeResultados

		try:
			return round((EBIT_ / Activos) * 100, 2)
		except Exception as e:
			# print(e)
			return None

	def P_ACTIVO(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		try:
			date = round(date.last().preco_da_acao, 2)
			Activos = round(self.Activos(), 2)
			return round(date / Activos, 2)
		except Exception as e:
			# print(e)
			return None

	def P_EBITDA(self):
		return None

	def P_EBIT(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		try:
			date = round(date.last().preco_da_acao, 2)
			EBIT = round(self.EBIT_(), 2)
			return round(date / EBIT, 2)
		except Exception as e:
			# print(e)
			return None

	def P_VPA(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		try:
			date = round(date.last().preco_da_acao, 2)
			VPL = round(self.VPL(), 2)
			return round(date / VPL, 2)
		except Exception as e:
			# print(e)
			return None

	def P_L(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		try:
			date = round(date.last().preco_da_acao, 2)
			LPA = round(self.LPA(), 2)
			return round(date / LPA, 2)
		except Exception as e:
			# print(e)
			return None

	def Capital_de_Giro_Liquido(self):
		try:
			activo_corrente = Balanco.objects.get(ano=self.ano).activo_corrente
			passivo_corrente = Balanco.objects.get(ano=self.ano).passivo_corrente
			passivo_nao_corrente = Balanco.objects.get(ano=self.ano).passivo_nao_corrente
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
			result = round(((activo_corrente - passivo_corrente - passivo_nao_corrente) / numero_medio_ponderado_de_acoes), 2)
			return result
		except Exception as e:
			# print(e)
			return None

	def Capital_de_Giro(self):
		try:
			activo_corrente = Balanco.objects.get(ano=self.ano).activo_corrente
			passivo_corrente = Balanco.objects.get(ano=self.ano).passivo_corrente
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
			result = round(((activo_corrente - passivo_corrente) / numero_medio_ponderado_de_acoes), 2)
			return result
		except Exception as e:
			# print(e)
			return None

	def Vendas_Liquidas(self):
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano).vendas
		numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
		try:
			result = round(vendas / numero_medio_ponderado_de_acoes, 2)
			return result
		except Exception as e:
			# print(e)
			return None

	def Activos(self):
		total_de_activo = Balanco.objects.get(ano=self.ano).total_de_activo()
		numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
		try:
			result = round(total_de_activo / numero_medio_ponderado_de_acoes, 2)
			return result
		except Exception as e:
			print(self.ano)
			# print(e)
			return None

	def EBITDA_(self):
		return 'Sem registo'

	def EBIT_(self):
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano).EBIT
		numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
		try:
			result = round(EBIT / numero_medio_ponderado_de_acoes, 2)
			return result
		except Exception as e:
			print(self.ano)
			# print(e)
			return None

	def VPL(self):
		total_do_capital_proprio = Balanco.objects.get(ano=self.ano).total_do_capital_proprio()
		numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
		try:
			result = round(total_do_capital_proprio / numero_medio_ponderado_de_acoes, 2)
			return result
		except Exception as e:
			print(self.ano)
			# print(e)
			return None

	def LPA(self):
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano).numero_medio_ponderado_de_acoes
		try:
			result = round(lucro_liquido_depois_de_imposto / numero_medio_ponderado_de_acoes, 2)
			return result
		except Exception as e:
			print(self.ano)
			# print(e)
			return None


class IndicadoresDeEndividamento(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)

	class Meta:
		ordering = ('ano',)

	def Divida_Bruta_Lucro_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano)
		divida_bruta = TableDeDivida.objects.get(balanco=balanco).divida_bruta
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		try:
			result = round(divida_bruta / lucro_liquido_depois_de_imposto, 2)
			return result
		except Exception as e:
			# print(e)
			return None

	def Divida_Liquido_Lucro_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano)
		divida_liquida = TableDeDivida.objects.get(balanco=balanco).divida_liquida()
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		try:
			return round(divida_liquida / lucro_liquido_depois_de_imposto, 2)
		except Exception as e:
			# print(e)
			return None

	def Divida_Liquido_EBITDA(self):
		return 'Sem registo'

	def Divida_Liquido_EBITD(self):
		balanco = Balanco.objects.get(ano=self.ano)
		divida_liquida = TableDeDivida.objects.get(balanco=balanco).divida_liquida()
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano).EBIT
		try:
			return round(divida_liquida / EBIT, 2)
		except Exception as e:
			# print(e)
			return None

	def Divida_Patrimonio_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano)
		divida_liquida = TableDeDivida.objects.get(balanco=balanco).divida_liquida()
		total_do_capital_proprio = Balanco.objects.get(ano=self.ano).total_do_capital_proprio()
		try:
			return round(divida_liquida / total_do_capital_proprio, 2)
		except Exception as e:
			# print(e)
			return None

	def Divida_or_Activo_Total(self):
		balanco = Balanco.objects.get(ano=self.ano)
		divida_liquida = TableDeDivida.objects.get(balanco=balanco).divida_liquida()
		total_de_activo = Balanco.objects.get(ano=self.ano).total_de_activo()
		try:
			return round(divida_liquida / total_de_activo, 2)
		except Exception as e:
			# print(e)
			return None

	def Liquidez_Geral(self):
		total_de_activo = Balanco.objects.filter(ano=self.ano)
		total_de_passivo = Balanco.objects.filter(ano=self.ano)
		try:
			total_de_activo = total_de_activo.first().total_de_activo()
			total_de_passivo = total_de_passivo.first().total_de_passivo()
			return round(total_de_activo / total_de_passivo, 2)
		except Exception as e:
			# print(e)
			return None

	def Liquidez_Seca(self):
		activo_corrente = Balanco.objects.filter(ano=self.ano)
		inventarios = Balanco.objects.filter(ano=self.ano)
		passivo_corrente = Balanco.objects.filter(ano=self.ano)
		try:
			activo_corrente = activo_corrente.first().activo_corrente
			inventarios = inventarios.first().inventarios
			passivo_corrente = passivo_corrente.first().passivo_corrente
			return round((activo_corrente - inventarios) / passivo_corrente, 2)
		except Exception as e:
			# print(e)
			return None

	def Liquidez_Corrente(self):
		activo_corrente = Balanco.objects.filter(ano=self.ano)
		passivo_corrente = Balanco.objects.filter(ano=self.ano)
		try:
			activo_corrente = activo_corrente.first().activo_corrente
			passivo_corrente = passivo_corrente.first().passivo_corrente
			return round(activo_corrente / passivo_corrente, 2)
		except Exception as e:
			# print(e)
			return None


class IndicadoresDeCrescimento(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)

	class Meta:
		ordering = ('ano',)

	def CAGR_Receita_5A(self):
		year = int(self.ano)
		vendas_agora = DemonstracaoDeResultados.objects.filter(ano=year)
		vendas_ha_5_anos = DemonstracaoDeResultados.objects.filter(ano=year-4)
		try:
			vendas_agora = vendas_agora.first().vendas
			print(f'vendas_agora = {vendas_agora}')
			vendas_ha_5_anos = vendas_ha_5_anos.first().vendas
			print(f'vendas_ha_5_anos = {vendas_ha_5_anos}')
			return round(((float(vendas_agora / vendas_ha_5_anos) ** (1/4)) - 1) * 100, 2)
		except Exception as e:
			# print(e)
			return None


	def CAGR_Lucro_5A(self):
		year = int(self.ano)
		lucro_liquido_depois_de_imposto_agora = DemonstracaoDeResultados.objects.filter(ano=year)
		lucro_liquido_depois_de_imposto_ha_5_anos = DemonstracaoDeResultados.objects.filter(ano=year-4)
		try:
			lucro_liquido_depois_de_imposto_agora = lucro_liquido_depois_de_imposto_agora.first().lucro_liquido_depois_de_imposto
			print(f'lucro_liquido_depois_de_imposto_agora = {lucro_liquido_depois_de_imposto_agora}')
			lucro_liquido_depois_de_imposto_ha_5_anos = lucro_liquido_depois_de_imposto_ha_5_anos.first().lucro_liquido_depois_de_imposto
			print(f'lucro_liquido_depois_de_imposto_ha_5_anos = {lucro_liquido_depois_de_imposto_ha_5_anos}')
			return round(((float(lucro_liquido_depois_de_imposto_agora / lucro_liquido_depois_de_imposto_ha_5_anos) ** (1/4)) - 1) * 100, 2)
		except Exception as e:
			# print(e)
			return None



	def CAGR_Receita_5A(self):
		year = int(self.ano)
		vendas_agora = DemonstracaoDeResultados.objects.filter(ano=year)
		vendas_ha_5_anos = DemonstracaoDeResultados.objects.filter(ano=year-4)
		try:
			vendas_agora = vendas_agora.first().vendas
			print(f'vendas_agora = {vendas_agora}')
			vendas_ha_5_anos = vendas_ha_5_anos.first().vendas
			print(f'vendas_ha_5_anos = {vendas_ha_5_anos}')
			return round(((float(vendas_agora / vendas_ha_5_anos) ** (1/4)) - 1) * 100, 2)
		except Exception as e:
			# print(e)
			return None


class IndicadoresDeEficiencia(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)

	class Meta:
		ordering = ('id',)

	def margem_bruta(self):
		lucros_bruto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucros_bruto
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano).vendas
		try:
			return round((lucros_bruto / vendas) * 100, 2)
		except Exception as e:
			return None

	def margin_EBITIDA(self):
		return 'Sem registo'

	def margin_EBIT(self):
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano).EBIT
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano).vendas
		try:
			return round((EBIT / vendas) * 100, 2)
		except Exception as e:
			return None

	def margin_Liquida(self):
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano).vendas
		try:
			return round((lucro_liquido_depois_de_imposto / vendas) * 100, 2)
		except Exception as e:
			return None


class IndicadoresDeRentabilidade(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)

	class Meta:
		ordering = ('id',)

	def ROA(self):
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		total_de_activo = Balanco.objects.get(ano=self.ano).total_de_activo()
		try:
			return round((lucro_liquido_depois_de_imposto / total_de_activo) * 100, 2)
		except Exception as e:
			return None

	def ROE(self):
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		total_do_capital_proprio = Balanco.objects.get(ano=self.ano).total_do_capital_proprio()
		try:
			return round((lucro_liquido_depois_de_imposto / total_do_capital_proprio) * 100, 2)
		except Exception as e:
			return None

	def Roic(self):
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano).EBIT
		lucro_antes_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_antes_de_imposto
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano).lucro_liquido_depois_de_imposto
		balanco = Balanco.objects.get(ano=self.ano)
		total_do_capital_proprio = balanco.total_do_capital_proprio()
		divida_bruta = TableDeDivida.objects.get(balanco=balanco).divida_bruta
		
		try:
			return round(((
				EBIT - (lucro_antes_de_imposto - lucro_liquido_depois_de_imposto)
			) / (
				total_do_capital_proprio  + divida_bruta
			)) * 100, 2)
		except Exception as e:
			return None

	def Giro_dos_Activos(self):
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano).vendas
		total_de_activo = Balanco.objects.get(ano=self.ano).total_de_activo()
		
		try:
			return round(vendas / total_de_activo, 2)
		except Exception as e:
			return None


class DemonstracaoDeFluxoDeCaixa(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)
	fundos_gerados_das_actividades_operacionais = models.DecimalField(
		max_digits=20, decimal_places=2, blank=True)
	fundos_utilizados_em_actividades_de_investimento = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	fundos_introduzidos_atraves_de_actividades_de_financiamento = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

	def __str__(self):
		return f'{self.ano}'

	def fluxo_de_caixa(self):
		return (self.fundos_gerados_das_actividades_operacionais + 
				self.fundos_utilizados_em_actividades_de_investimento +
			    self.fundos_introduzidos_atraves_de_actividades_de_financiamento +
			    self.acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa)

	class Meta:
		verbose_name_plural = 'Demonstracao De Fluxo De Caixa'
		verbose_name_plural = 'Demonstracao De Fluxos De Caixas'


class TableDeDivida(models.Model):
	balanco = models.OneToOneField(to='Balanco',
		on_delete=models.CASCADE, unique=True)
	divida_bruta = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

	def __str__(self):
		return 'Table de Divida'

	class Meta:
		verbose_name = 'Table De Divida'
		verbose_name_plural = 'Table De Divida'

	def divida_liquida(self):
		return self.divida_bruta - self.balanco.caixa

class DemonstracaoDeResultados(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)
	vendas = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucros_bruto = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	EBITIDA = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	EBIT = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucro_antes_de_imposto = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucro_liquido_depois_de_imposto = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	dividendo_declarados_e_pagos = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	numero_medio_ponderado_de_acoes = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	
	def __str__(self):
		return f'{self.ano} - {self.vendas}'

	def impostos(self):
		return self.lucro_antes_de_imposto - self.lucro_liquido_depois_de_imposto

	def lucro_por_acao(self):
		return round(self.lucro_liquido_depois_de_imposto / self.numero_medio_ponderado_de_acoes, 2)

	def dividendo_por_acao(self):
		return round(self.dividendo_declarados_e_pagos / self.numero_medio_ponderado_de_acoes, 2)

	class Meta:
		verbose_name = 'Demonstracao De Resultados'
		verbose_name_plural = 'Demonstracao De Resultados'


class Balanco(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015', unique=True)
	activo_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	caixa = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	inventarios = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	activo_nao_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	passivo_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	passivo_nao_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	capital_social = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	premio_de_emissao = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	reservas_nao_distribuidas = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucros_acumulados = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

	def __str__(self):
		return self.ano

	class Meta:
		verbose_name = 'Balanco'
		verbose_name_plural = 'Balancos'

	def total_de_activo(self):
		return self.activo_corrente + self.activo_nao_corrente

	def total_de_passivo(self):
		return self.passivo_corrente + self.passivo_nao_corrente

	def total_do_capital_proprio(self):
		return self.capital_social + self.premio_de_emissao + self.reservas_nao_distribuidas + self.lucros_acumulados

	def total_do_passvo_e_capital_proprio(self):
		return self.total_de_passivo() + self.total_do_capital_proprio()

class Client(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	user = models.ForeignKey(to=User,
		on_delete=models.CASCADE,
		blank=True, null=True)
	email = models.EmailField()
	phone_number = models.CharField(max_length=50)
	location = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.last_name.upper()}, {self.first_name}'

	class Meta:
		ordering = ('id',)
		verbose_name = 'Client'
		verbose_name_plural = 'Clients'


