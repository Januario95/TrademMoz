from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta


class Company(models.Model):
	SECTOR = (
		('bebidas', 'Bebidas'),
		('seguros', 'Seguros'),
		('servicos-de-software', 'Servicos de Software'),
		('financeiro', 'Financeiro'),
		('petroleo-e-gas', 'Petroleo e Gas'),
		('comercio', 'Comercio'),
		('energia-hidroelectrica', 'Energia Hidroelectrica'),
		('portagem', 'Portagem'),
	)
	name = models.CharField(
		max_length=125, default='CDM',
		unique=True)
	sector_de_actuacao = models.CharField(
		max_length=100, choices=SECTOR,
		default='bebidas')

	def __str__(self):
		return f'{self.name}'

	class Meta:
		ordering = ('id',)
		verbose_name = 'Company'
		verbose_name_plural = 'Companies'

	def serialize(self):
		data = {
			'id': self.id,
			'name': self.name
		}

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

	def P_L(self):
		try:
			year = self.date.strftime('%Y')
			accao = CotacoesDasAcoes.objects.get(
				date=self.date,
				nome_da_empresa=self.nome_da_empresa
			) # .last()
			value = DemonstracaoDeResultados.objects.filter(
				nome_da_empresa=self.nome_da_empresa).last()
			# print(value)
			result = accao.preco_da_acao / value.lucro_por_acao()
			return round(result, 4)
		except Exception as e:
			# print(e.args)
			return None

	def dividendo_por_acao_ultimo_valor(self, nome_da_empresa):
		try:
			# year = datetime.strptime(self.date, '%Y').date().year
			year = self.date.strftime('%Y')
			value = DemonstracaoDeResultados.objects.filter(
				# ano=int(year),
				nome_da_empresa=nome_da_empresa).last()

			value = value.dividendo_declarados_e_pagos / value.numero_medio_ponderado_de_acoes
			return round(value, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Variacao_Semestral(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=180),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Variacao_Mensal(self):
		try:
			preco_da_acao_actual = self.preco_da_acao
			preco_da_acao_a_30_dias = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=30),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			# print(f'date_de_hoje = {self.date}')
			# print(f'date_a_30_dias = {self.date-timedelta(days=30)}')
			# print(f'preco_da_acao_actual = {preco_da_acao_actual}')
			# print(f'preco_da_acao_a_30_dias = {preco_da_acao_a_30_dias}')
			first = preco_da_acao_actual / preco_da_acao_a_30_dias
			result = round(((first - 1) * 100), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Variacao_Semanal(self):
		try:
			preco_da_acao_actual = self.preco_da_acao
			preco_da_acao_a_sete_dias = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=6),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			# print(f'date_de_hoje = {self.date}')
			# print(f'date_a_sete_dias = {self.date-timedelta(days=7)}')
			# print(f'preco_da_acao_actual = {preco_da_acao_actual}')
			# print(f'preco_da_acao_a_sete_dias = {preco_da_acao_a_sete_dias}')
			first = preco_da_acao_actual / preco_da_acao_a_sete_dias
			result = round(((first - 1) * 100), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Variacao_Diaria(self):
		try:
			preco_da_acao_hoje = self.preco_da_acao
			preco_da_acao_ontem = CotacoesDasAcoes.objects.get(
				date=self.date-timedelta(days=1),
				nome_da_empresa=self.nome_da_empresa
			).preco_da_acao
			first = preco_da_acao_hoje / preco_da_acao_ontem
			result = round(((first - 1) * 100), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def EV_EBIT(self):
		try:
			EBIT = DemonstracaoDeResultados.objects.filter(
				ano=int(self.date.year)-1,
				nome_da_empresa=self.nome_da_empresa)
			if EBIT.exists():
				# print('EXISTS')
				EBIT = EBIT.first()
				EBIT = EBIT.EBIT
				# print(f'EBIT = {EBIT}')
				# print(f'EV = {self.EV()}')
				result = self.EV() / EBIT
				# print(f'EV_EBIT = {result}')
				return round(result, 4)
			else:
				# print('DOES NOT EXIST')
				return None
		except Exception as e:
			# print(e)
			return None

	def EV(self):
		try:
			balanco = Balanco.objects.last() # get(ano=self.date.year-1)
			# print(f'ano = {self.date}')
			divida_liquida = TableDeDivida.objects.filter(
				# ano.self.date.year,
				nome_da_empresa=self.nome_da_empresa
			).last().divida_liquida()
			Valor_Do_Mercado = self.Valor_Do_Mercado()
			# print(f'divida_liquida = {divida_liquida}')
			# print(f'Valor_Do_Mercado = {Valor_Do_Mercado}')
			result = divida_liquida + Valor_Do_Mercado
			# print(f'EV = {result}')
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Valor_Do_Mercado(self):
		try:
			accoes = CotacoesDasAcoes.objects.get(
				date=self.date,
				nome_da_empresa=self.nome_da_empresa
			)
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.filter(
				ano=int(self.date.year)-1,
				nome_da_empresa=self.nome_da_empresa)# .numero_medio_ponderado_de_acoes
			# print(f'DATE = {self.date}')
			if numero_medio_ponderado_de_acoes.exists():
				# print('EXISTS')
				numero_medio_ponderado_de_acoes = numero_medio_ponderado_de_acoes.first().numero_medio_ponderado_de_acoes
				return self.preco_da_acao * numero_medio_ponderado_de_acoes
			else:
				return None
				# print('DOES NOT EXIST')
		except Exception as e:
			# print('ERROR STARTS HERE')
			# print(e.args)
			# print('ERROR ENDS HERE')
			return None


class MetricasPorAccao(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(
		to=Company, on_delete=models.CASCADE,
		blank=True)
	# nome_da_empresa = models.CharField(
	# 	max_length=150, blank=True,
	# 	default='CDM')

	class Meta:
		ordering = ('-ano',)

	def P_Capital_De_Giro_Liquido(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		Capital_de_Giro_Liquido = self.Capital_de_Giro_Liquido()
		try:
			date = round(date.last().preco_da_acao, 4)
			return round(date / Capital_de_Giro_Liquido, 4)
		except Exception as e:
			# print(e.args)
			return None

	def P_Capital_De_Giro(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
				nome_da_empresa=nome_da_empresa
			)
			Capital_de_Giro = self.Capital_de_Giro()
		
			date = round(date.last().preco_da_acao, 4)
			return round(date / Capital_de_Giro, 4)
		except Exception as e:
			# print(e.args)
			return None

	def PSR(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
				nome_da_empresa=nome_da_empresa
			)
			Vendas_Liquidas = self.Vendas_Liquidas()

			date = round(date.last().preco_da_acao, 4)
			return round(date / Vendas_Liquidas, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Dividend_Yield(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
			)
			dividendo_por_acao = DemonstracaoDeResultados.objects.get(ano=year,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).dividendo_por_acao()

			date = round(date.last().preco_da_acao, 4)
			return round((dividendo_por_acao / date) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def EBIT_ACTIVOS(self):
		try:
			EBIT_ = self.EBIT_()
			Activos = self.Activos()
			result =  round((EBIT_ / Activos) * 100, 4)
			# print(f'EBIT = {EBIT_}.\tActivos = {Activos}.\tEBIT_ACTIVOS = {result}')
			return result
		except Exception as e:
			# print(e.args)
			return None

	def P_ACTIVO(self):
		year = datetime.strptime(self.ano, '%Y').date().year
		nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
		date = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=nome_da_empresa
		)
		try:
			date = round(date.last().preco_da_acao, 4)
			Activos = round(self.Activos(), 4)
			return round(date / Activos, 4)
		except Exception as e:
			# print(e.args)
			return None

	def P_EBITDA(self):
		return None

	def P_EBIT(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
				nome_da_empresa=nome_da_empresa
			)

			date = round(date.last().preco_da_acao, 4)
			EBIT = round(self.EBIT_(), 4)
			return round(date / EBIT, 4)
		except Exception as e:
			# print(e.args)
			return None

	def VPA(self):
		# print('VPA')
		# print(f'ANO = {self.ano}')
		try:
			total_do_capital_proprio = Balanco.objects.filter(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).last().total_do_capital_proprio()
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.filter(ano=self.ano,
					nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).last().numero_medio_ponderado_de_acoes
			result = total_do_capital_proprio / numero_medio_ponderado_de_acoes
			# print(f'total_do_capital_proprio = {total_do_capital_proprio}')
			# print(f'numero_medio_ponderado_de_acoes = {numero_medio_ponderado_de_acoes}')
			return result
		except Exception as e:
			# print(e.args)
			return None

	def P_VPA(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
				nome_da_empresa=nome_da_empresa
			)

			date = round(date.last().preco_da_acao, 4)
			VPL = round(self.VPL(), 4)
			return round(date / VPL, 4)
		except Exception as e:
			# print(e.args)
			return None

	def P_L(self):
		try:
			year = datetime.strptime(self.ano, '%Y').date().year
			nome_da_empresa = Company.objects.get(name=self.nome_da_empresa)
			date = CotacoesDasAcoes.objects.filter(
				nome_da_empresa=nome_da_empresa
			)
			date = round(date.last().preco_da_acao, 4)
			LPA = round(self.LPA(), 4)
			result = round(date / LPA, 4)
			# print(f'preco_da_acao = {date}.\tLPA = {LPA}.\tP_L = {result}')
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Capital_de_Giro_Liquido(self):
		try:
			activo_corrente = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).activo_corrente
			passivo_corrente = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).passivo_corrente
			passivo_nao_corrente = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).passivo_nao_corrente
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
			result = round(((activo_corrente - passivo_corrente - passivo_nao_corrente) / numero_medio_ponderado_de_acoes), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Capital_de_Giro(self):
		try:
			activo_corrente = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).activo_corrente
			passivo_corrente = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).passivo_corrente
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
			result = round(((activo_corrente - passivo_corrente) / numero_medio_ponderado_de_acoes), 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Vendas_Liquidas(self):
		try:
			vendas = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).vendas
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
		
			result = round(vendas / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Activos(self):
		try:
			total_de_activo = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_de_activo()
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
		
			result = round(total_de_activo / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def EBITDA_(self):
		return 'Sem registo'

	def EBIT_(self):
		try:
			EBIT = DemonstracaoDeResultados.objects.get(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).EBIT
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
		
			result = round(EBIT / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def VPL_Nas_Acoes(self, nome_da_empresa):
		try:
			total_do_capital_proprio_ = Balanco.objects.filter(
			nome_da_empresa=Company.objects.get(name=nome_da_empresa)).last()
			total_do_capital_proprio = total_do_capital_proprio_.total_do_capital_proprio()
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.filter(
				nome_da_empresa=Company.objects.get(name=nome_da_empresa)).last().numero_medio_ponderado_de_acoes

			result = round(total_do_capital_proprio / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print('ERROR HERE...')
			# print(e.args)
			return None

	def VPL(self):
		try:
			total_do_capital_proprio = Balanco.objects.get(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_do_capital_proprio()
			numero_medio_ponderado_de_acoes = DemonstracaoDeResultados.objects.get(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).numero_medio_ponderado_de_acoes
		
			result = round(total_do_capital_proprio / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def LPA(self):
		try:
			obj = DemonstracaoDeResultados.objects.filter(
			ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).last()
			lucro_liquido_depois_de_imposto = obj.lucro_liquido_depois_de_imposto
			numero_medio_ponderado_de_acoes = obj.numero_medio_ponderado_de_acoes
			result = round(lucro_liquido_depois_de_imposto / numero_medio_ponderado_de_acoes, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None


class IndicadoresDeEndividamento(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.ano} - {self.nome_da_empresa}'

	class Meta:
		ordering = ('ano',)

	def Divida_Bruta_Lucro_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
		divida_bruta = TableDeDivida.objects.get(
			ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).divida_bruta
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_liquido_depois_de_imposto
		try:
			result = round(divida_bruta / lucro_liquido_depois_de_imposto, 4)
			return result
		except Exception as e:
			# print(e.args)
			return None

	def Divida_Liquido_Lucro_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
		divida_liquida = TableDeDivida.objects.get(
			ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).divida_liquida()
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_liquido_depois_de_imposto
		try:
			return round(divida_liquida / lucro_liquido_depois_de_imposto, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Divida_Liquido_EBITDA(self):
		return 'Sem registo'

	def Divida_Liquido_EBITD(self):
		balanco = Balanco.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
		divida_liquida = TableDeDivida.objects.get(
			ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).divida_liquida()
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).EBIT
		try:
			return round(divida_liquida / EBIT, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Divida_Patrimonio_Liquido(self):
		balanco = Balanco.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
		divida_liquida = TableDeDivida.objects.get(
			ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).divida_liquida()
		total_do_capital_proprio = Balanco.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_do_capital_proprio()
		print(f'\nANO = {self.ano}')
		print(f'divida_liquida = {divida_liquida}')
		print(f'total_do_capital_proprio = {total_do_capital_proprio}')
		try:
			result = round(divida_liquida / total_do_capital_proprio, 4)
			print(f'result = {result}')
			return result
		except Exception as e:
			print('ERROR HERE...')
			print(e.args)
			return None

	def Divida_or_Activo_Total(self):
		try:
			balanco = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
			divida_liquida = TableDeDivida.objects.get(
				ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).divida_liquida()
			total_de_activo = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_de_activo()
			return round(divida_liquida / total_de_activo, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Liquidez_Geral(self):
		try:
			obj = Balanco.objects.get(
				ano=self.ano,
				nome_da_empresa=self.nome_da_empresa)
			# total_de_activo = Balanco.objects.filter(ano=self.ano)
			# total_de_passivo = Balanco.objects.filter(ano=self.ano)
			# total_de_activo = total_de_activo.first().total_de_activo()
			# total_de_passivo = total_de_passivo.first().total_de_passivo()

			total_de_activo = obj.total_de_activo()
			total_de_passivo = obj.total_de_passivo()
			return round(total_de_activo / total_de_passivo, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Liquidez_Seca(self):
		try:
			obj = Balanco.objects.get(
				ano=self.ano,
				nome_da_empresa=self.nome_da_empresa)
			# inventarios = Balanco.objects.filter(ano=self.ano)
			# passivo_corrente = Balanco.objects.filter(ano=self.ano)
			# activo_corrente = activo_corrente.first().activo_corrente
			# inventarios = inventarios.first().inventarios
			# passivo_corrente = passivo_corrente.first().passivo_corrente
			activo_corrente = obj.activo_corrente
			inventarios = obj.inventarios
			passivo_corrente = obj.passivo_corrente
			return round((activo_corrente - inventarios) / passivo_corrente, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Liquidez_Corrente(self):
		try:
			obj = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=self.nome_da_empresa)
			# activo_corrente = Balanco.objects.filter(ano=self.ano)
			# passivo_corrente = Balanco.objects.filter(ano=self.ano)
			# activo_corrente = activo_corrente.first().activo_corrente
			# passivo_corrente = passivo_corrente.first().passivo_corrente
			activo_corrente = obj.activo_corrente
			passivo_corrente = obj.passivo_corrente
			return round(activo_corrente / passivo_corrente, 4)
		except Exception as e:
			# print(e.args)
			return None


class IndicadoresDeCrescimento(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.ano} - {self.nome_da_empresa}'

	class Meta:
		ordering = ('ano',)

	def CAGR_Receita_5A(self):
		try:
			year = int(self.ano)
			vendas_agora = DemonstracaoDeResultados.objects.filter(
				ano=year,
				nome_da_empresa=self.nome_da_empresa)
			vendas_ha_5_anos = DemonstracaoDeResultados.objects.filter(
				ano=year-4,
				nome_da_empresa=self.nome_da_empresa)
			# print(f'ANO-ACTUAL = {year}')
			# print(f'ANO-A-5-ANOS = {year-4}')
			vendas_agora = vendas_agora.first().vendas
			# print(f'vendas_agora = {vendas_agora}')
			vendas_ha_5_anos = vendas_ha_5_anos.first().vendas
			# print(f'vendas_ha_5_anos = {vendas_ha_5_anos}')
			return round(((float(vendas_agora / vendas_ha_5_anos) ** (1/4)) - 1) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None


	def CAGR_Lucro_5A(self):
		try:
			year = int(self.ano)
			lucro_liquido_depois_de_imposto_agora = DemonstracaoDeResultados.objects.filter(
				ano=year,
				nome_da_empresa=self.nome_da_empresa)
			lucro_liquido_depois_de_imposto_ha_5_anos = DemonstracaoDeResultados.objects.filter(
				ano=year-4,
				nome_da_empresa=self.nome_da_empresa)
			print(f'ANO-ACTUAL = {year}')
			print(f'ANO-A-5-ANOS = {year-4}')
			lucro_liquido_depois_de_imposto_agora = lucro_liquido_depois_de_imposto_agora.first().lucro_liquido_depois_de_imposto
			print(f'lucro_liquido_depois_de_imposto_agora = {lucro_liquido_depois_de_imposto_agora}')
			lucro_liquido_depois_de_imposto_ha_5_anos = lucro_liquido_depois_de_imposto_ha_5_anos.first().lucro_liquido_depois_de_imposto
			print(f'lucro_liquido_depois_de_imposto_ha_5_anos = {lucro_liquido_depois_de_imposto_ha_5_anos}')
			return round(((float(lucro_liquido_depois_de_imposto_agora / lucro_liquido_depois_de_imposto_ha_5_anos) ** (1/4)) - 1) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None


class IndicadoresDeEficiencia(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.nome_da_empresa} - {self.ano}'

	class Meta:
		ordering = ('id',)

	def margem_bruta(self):
		lucros_bruto = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucros_bruto
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).vendas
		try:
			return round((lucros_bruto / vendas) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def margin_EBITIDA(self):
		return 'Sem registo'

	def margin_EBIT(self):
		EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).EBIT
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).vendas
		try:
			return round((EBIT / vendas) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def margin_Liquida(self):
		lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_liquido_depois_de_imposto
		vendas = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).vendas
		try:
			return round((lucro_liquido_depois_de_imposto / vendas) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None


class IndicadoresDeRentabilidade(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(
		to=Company, on_delete=models.CASCADE,
		blank=True, null=True)

	def __str__(self):
		return f'{self.ano} - {self.nome_da_empresa}'

	class Meta:
		ordering = ('id',)

	def ROA(self):
		try:
			lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_liquido_depois_de_imposto
			total_de_activo = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_de_activo()
			return round((lucro_liquido_depois_de_imposto / total_de_activo) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def ROE(self):
		try:
			lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.filter(
				ano=self.ano, nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)
			).last()
			total_do_capital_proprio = Balanco.objects.filter(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).last()

			total_do_capital_proprio = total_do_capital_proprio.total_do_capital_proprio()
			lucro_liquido_depois_de_imposto = lucro_liquido_depois_de_imposto.lucro_liquido_depois_de_imposto
			return round((lucro_liquido_depois_de_imposto / total_do_capital_proprio) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Roic(self):
		try:
			EBIT = DemonstracaoDeResultados.objects.get(ano=self.ano,
			nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).EBIT
			lucro_antes_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_antes_de_imposto
			lucro_liquido_depois_de_imposto = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).lucro_liquido_depois_de_imposto
			balanco = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa))
			total_do_capital_proprio = balanco.total_do_capital_proprio()
			divida_bruta = TableDeDivida.objects.get(
				ano=self.ano,
				nome_da_empresa=self.nome_da_empresa
			).divida_bruta
			return round(((
				EBIT - (lucro_antes_de_imposto - lucro_liquido_depois_de_imposto)
			) / (
				total_do_capital_proprio  + divida_bruta
			)) * 100, 4)
		except Exception as e:
			# print(e.args)
			return None

	def Giro_dos_Activos(self):
		try:
			vendas = DemonstracaoDeResultados.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).vendas
			total_de_activo = Balanco.objects.get(ano=self.ano,
				nome_da_empresa=Company.objects.get(name=self.nome_da_empresa)).total_de_activo()

			return round(vendas / total_de_activo, 4)
		except Exception as e:
			# print(e.args)
			return None


class DemonstracaoDeFluxoDeCaixa(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)
	fundos_gerados_das_actividades_operacionais = models.DecimalField(
		max_digits=20, decimal_places=2, blank=True)
	fundos_utilizados_em_actividades_de_investimento = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	fundos_introduzidos_atraves_de_actividades_de_financiamento = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

	def __str__(self):
		return f'{self.nome_da_empresa} - {self.ano}'

	def fluxo_de_caixa(self):
		return (self.fundos_gerados_das_actividades_operacionais + 
				self.fundos_utilizados_em_actividades_de_investimento +
			    self.fundos_introduzidos_atraves_de_actividades_de_financiamento +
			    self.acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa)

	class Meta:
		verbose_name_plural = 'Demonstracao De Fluxo De Caixa'
		verbose_name_plural = 'Demonstracao De Fluxos De Caixas'


class TableDeDivida(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	# balanco = models.OneToOneField(to='Balanco',
	# 	on_delete=models.CASCADE, blank=True, null=True)
	nome_da_empresa = models.ForeignKey(
		to=Company, on_delete=models.CASCADE,
		blank=True, null=True)
	divida_bruta = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

	def __str__(self):
		return f'{self.ano} - {self.nome_da_empresa}'

	class Meta:
		verbose_name = 'Table De Divida'
		verbose_name_plural = 'Table De Divida'

	def divida_liquida(self):
		balanco = Balanco.objects.get(
			ano=self.ano,
			nome_da_empresa=self.nome_da_empresa)
		return self.divida_bruta - balanco.caixa

class DemonstracaoDeResultados(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)
	vendas = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
		default=0.0)
	lucros_bruto = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
		default=0.0)
	EBITIDA = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	EBIT = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucro_antes_de_imposto = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucro_liquido_depois_de_imposto = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	dividendo_declarados_e_pagos = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	numero_medio_ponderado_de_acoes = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	
	def __str__(self):
		return f'{self.ano} - {self.vendas}'

	def dividendo_por_acao(self):
		try:
			# year = self.date.strftime('%Y')
			# value = DemonstracaoDeResultados.objects.filter(
			# 	ano=int(year),
			# 	nome_da_empresa=self.nome_da_empresa)

			value = self.dividendo_declarados_e_pagos / self.numero_medio_ponderado_de_acoes
			return round(value, 4)
		except Exception as e:
			# print(e.args)
			return None

	def impostos(self):
		return self.lucro_antes_de_imposto - self.lucro_liquido_depois_de_imposto

	def lucro_por_acao(self):
		return round(self.lucro_liquido_depois_de_imposto / self.numero_medio_ponderado_de_acoes, 4)

	def dividendo_por_acao(self):
		return round(self.dividendo_declarados_e_pagos / self.numero_medio_ponderado_de_acoes, 4)

	class Meta:
		verbose_name = 'Demonstracao De Resultados'
		verbose_name_plural = 'Demonstracao De Resultados'


class Balanco(models.Model):
	ano = models.CharField(
		max_length=50, blank=True,
		default='2015')
	nome_da_empresa = models.ForeignKey(to=Company,
		on_delete=models.CASCADE, blank=True, null=True)
	activo_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	caixa = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	inventarios = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	activo_nao_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	passivo_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	passivo_nao_corrente = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	capital_social = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	premio_de_emissao = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
		)
	reservas_nao_distribuidas = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	lucros_acumulados = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
	disconto_de_premio_das_acoes_proprias = models.DecimalField(
		max_digits=20, decimal_places=2, default=-1.0)
	resultados_transitado = models.DecimalField(
		max_digits=20, decimal_places=2, default=-1.0)
	resultados_de_exercicio = models.DecimalField(
		max_digits=20, decimal_places=2, default=-1.0)


	def __str__(self):
		return self.ano

	class Meta:
		verbose_name = 'Balanco'
		verbose_name_plural = 'Balancos'

	def disconto_e_premio_das_acoes_proprias_(self):
		if (self.nome_da_empresa.name == 'CDM' or 
			self.nome_da_empresa.name == 'Arco Investimentos'):
			return self.premio_de_emissao
		else:
			return self.disconto_de_premio_das_acoes_proprias

	def lucros_acumulados_geral(self):
		if (self.nome_da_empresa.name == 'Hidroelectrica de Cahora Bassa' or
			self.nome_da_empresa.name == 'Arco Investimentos'):
			return self.lucros_acumulados_2()
		else:
			return self.lucros_acumulados

	def lucros_acumulados_2(self):
		return self.resultados_de_exercicio + self.resultados_transitado

	def total_de_activo(self):
		return self.activo_corrente + self.activo_nao_corrente

	def total_de_passivo(self):
		return self.passivo_corrente + self.passivo_nao_corrente

	def total_do_capital_proprio(self):
		return self.capital_social + self.disconto_e_premio_das_acoes_proprias_() + self.reservas_nao_distribuidas + self.lucros_acumulados_geral() 

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


