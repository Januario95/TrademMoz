from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
	Client, Balanco,
	TableDeDivida, DemonstracaoDeResultados,
	DemonstracaoDeFluxoDeCaixa,
	IndicadoresDeRentabilidade,
	IndicadoresDeEficiencia,
	IndicadoresDeCrescimento,
	IndicadoresDeEndividamento,
	MetricasPorAccao,
	CotacoesDasAcoes,
	Company,
)


def format_value(value, symbol='MZN'):
	if value is None:
		return 'Sem registo'
	if value == 0:
		return 'Sem registo'
	if symbol == 'MZN':
		return mark_safe(f'{symbol} {value}')
	return mark_safe(f'{value}%')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    # list_filter = ('',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)


@admin.register(CotacoesDasAcoes)
class CotacoesDasAcoesdmin(admin.ModelAdmin):
	list_display = ['id', 'date', 'nome_da_empresa',
					'preco_da_acao', 'Valor_Do_Mercado_',
					'EV_', 'Variacao_Diaria_', 'Variacao_Semanal_',
					'Variacao_Mensal_', 'Variacao_Semestral_']

	list_per_page = 1000
	list_filter = ['nome_da_empresa',]
	search_fields = ['nome_da_empresa',]
	date_hierarchy = 'date'

	def Variacao_Semestral_(self, obj):
		if obj.Variacao_Semestral() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.Variacao_Semestral()}%')
	Variacao_Semestral_.short_description = 'Variacao Semestral'

	def Variacao_Mensal_(self, obj):
		if obj.Variacao_Mensal() is None:
			return 'Sem registo'
		# if obj.Variacao_Mensal() == 0:
		# 	return 'Sem registo'
		return mark_safe(f'{obj.Variacao_Mensal()}%')
	Variacao_Mensal_.short_description = 'Variacao Mensal'

	def Variacao_Semanal_(self, obj):
		if obj.Variacao_Semanal() is None:
			return 'Sem registo'
		# if obj.Variacao_Semanal() == 0:
		# 	return 'Sem registo'
		return mark_safe(f'{obj.Variacao_Semanal()}%')
	Variacao_Semanal_.short_description = 'Variacao Semanal'

	def Variacao_Diaria_(self, obj):
		if obj.Variacao_Diaria() is None:
			return 'Sem registo'
		# if obj.Variacao_Diaria() == 0:
		# 	return 'Sem registo'
		return mark_safe(f'{obj.Variacao_Diaria()}%')
	Variacao_Diaria_.short_description = 'Variacao Diaria'

	def EV_(self, obj):
		if obj.EV() is None:
			return 'Sem registo'
		if obj.EV() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.EV()}')
	EV_.short_description = 'EV'

	def Valor_Do_Mercado_(self, obj):
		if obj.Valor_Do_Mercado() is None:
			return 'Sem registo'
		if obj.Valor_Do_Mercado() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Valor_Do_Mercado()}')
	Valor_Do_Mercado_.short_description = 'Valor Do Mercado'

@admin.register(MetricasPorAccao)
class MetricasPorAccaoAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'nome_da_empresa', 'LPA_', 'VPL_',
					'EBIT_Func', 'EBITDA_Func',
					'Activos_', 'Vendas_Liquidas_',
					'Capital_de_Giro_',
					'Capital_de_Giro_Liquido_',
					'P_L_', 'P_VPA_', 'P_EBITDA_',
					'P_ACTIVO_', 'EBIT_ACTIVOS_',
					'Dividend_Yield_', 'PSR_',
					'EV_EBIT_', 'EV_EBITDA_',
					'P_Capital_De_Giro_',
					'P_Capital_De_Giro_Liquido_']

	def P_Capital_De_Giro_Liquido_(self, obj):
		if obj.P_Capital_De_Giro_Liquido() is None:
			return 'Sem registo'
		if obj.P_Capital_De_Giro_Liquido() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.P_Capital_De_Giro_Liquido()}')
	P_Capital_De_Giro_Liquido_.short_description = 'P Capital De Giro Liquido'

	def P_Capital_De_Giro_(self, obj):
		# value = format_value(obj.P_Capital_De_Giro())
		# return value
		if obj.P_Capital_De_Giro() is None:
			return 'Sem registo'
		if obj.P_Capital_De_Giro() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.P_Capital_De_Giro()}')
	P_Capital_De_Giro_.short_description = 'P Capital De Giro'

	def EV_EBITDA_(self, obj):
		if obj.EV_EBITDA() is None:
			return 'Sem registo'
		if obj.EV_EBITDA() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.EV_EBITDA()}')
	EV_EBITDA_.short_description = 'EV EBITDA'	

	def EV_EBIT_(self, obj):
		if obj.EV_EBIT() is None:
			return 'Sem registo'
		if obj.EV_EBIT() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.EV_EBIT()}')
	EV_EBIT_.short_description = 'EV EBIT'	

	def PSR_(self, obj):
		if obj.PSR() is None:
			return 'Sem registo'
		if obj.PSR() == 0:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.PSR()}')
	PSR_.short_description = 'Dividend Yield'

	def Dividend_Yield_(self, obj):
		if obj.Dividend_Yield() is None:
			return 'Sem registo'
		if obj.Dividend_Yield() == 0:
			return 'Sem registo'
		return mark_safe(f'{obj.Dividend_Yield()}%')
	Dividend_Yield_.short_description = 'Dividend Yield'

	def EBIT_ACTIVOS_(self, obj):
		if obj.EBIT_ACTOVOS() is None:
			return 'Sem registo'
		if obj.EBIT_ACTOVOS() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'{obj.EBIT_ACTOVOS()}%')
	EBIT_ACTIVOS_.short_description = 'EBIT ACTIVOS'

	def P_ACTIVO_(self, obj):
		if obj.P_ACTIVO() is None:
			return 'Sem registo'
		if obj.P_ACTIVO() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'MZN {obj.P_ACTIVO()}')
	P_ACTIVO_.short_description = 'P ACTIVO'

	def P_EBITDA_(self, obj):
		if obj.P_EBITDA() is None:
			return 'Sem registo'
		if obj.P_EBITDA() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'MZN {obj.P_EBITDA()}')
	P_EBITDA_.short_description = 'P EBITDA'

	def P_EBIT_(self, obj):
		if obj.P_EBIT() is None:
			return 'Sem registo'
		if obj.P_EBIT() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'MZN {obj.P_EBIT()}')
	P_EBIT_.short_description = 'P EBIT'

	def P_VPA_(self, obj):
		if obj.P_VPA() is None:
			return 'Sem registo'
		if obj.P_VPA() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'MZN {obj.P_VPA()}')
	P_VPA_.short_description = 'P VPA'

	def P_L_(self, obj):
		if obj.P_L() is None:
			return 'Sem registo'
		if obj.P_L() == 0:
			return 'Impossivel de calcular'
		return mark_safe(f'MZN {obj.P_L()}')
	P_L_.short_description = 'P L'

	def Capital_de_Giro_Liquido_(self, obj):
		if obj.Capital_de_Giro_Liquido() is None:
			return 'Sem registo'
		if obj.Capital_de_Giro_Liquido() == 0:
			return obj.Capital_de_Giro_Liquido()
		return mark_safe(f'MZN {obj.Capital_de_Giro_Liquido()}')
	Capital_de_Giro_Liquido_.short_description = 'Capital de Giro Liquido'

	def Capital_de_Giro_(self, obj):
		if obj.Capital_de_Giro() is None:
			return 'Sem registo'
		if obj.Capital_de_Giro() == 0:
			return obj.Capital_de_Giro()
		return mark_safe(f'MZN {obj.Capital_de_Giro()}')
	Capital_de_Giro_.short_description = 'Capital de Giro'

	def Vendas_Liquidas_(self, obj):
		if obj.Vendas_Liquidas() is None:
			return 'Sem registo'
		if obj.Vendas_Liquidas() == 0:
			return obj.Vendas_Liquidas()
		return mark_safe(f'MZN {obj.Vendas_Liquidas()}')
	Vendas_Liquidas_.short_description = 'Vendas Liquidas'

	def Activos_(self, obj):
		if obj.Activos() is None:
			return 'Sem registo'
		if obj.Activos() == 0:
			return obj.Activos()
		return mark_safe(f'MZN {obj.Activos()}')
	Activos_.short_description = 'Activos'

	def EBITDA_Func(self, obj):
		return obj.EBITDA_()
	EBITDA_Func.short_description = 'EBITDA'

	def EBIT_Func(self, obj):
		if obj.EBIT_() is None:
			return 'Sem registo'
		if obj.EBIT_() == 0:
			return obj.EBIT_()
		return mark_safe(f'MZN {obj.EBIT_()}')
	EBIT_Func.short_description = 'EBIT'

	def VPL_(self, obj):
		if obj.VPL() is None:
			return 'Sem registo'
		if obj.VPL() == 0:
			return obj.VPL()
		return mark_safe(f'MZN {obj.VPL()}')
	VPL_.short_description = 'VPL'

	def LPA_(self, obj):
		if obj.LPA() is None:
			return 'Sem registo'
		if obj.LPA() == 0:
			return obj.LPA()
		return mark_safe(f'MZN {obj.LPA()}')
	LPA_.short_description = 'LPA'

@admin.register(IndicadoresDeEndividamento)
class IndicadoresDeEndividamentoAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'Liquidez_Corrente_',
					'Liquidez_Seca_', 'Liquidez_Geral_',
					'Divida_or_Activo_Total_',
					'Divida_Patrimonio_Liquido_',
					'Divida_Liquido_EBITD_',
					'Divida_Liquido_EBITDA_',
					'Divida_Liquido_Lucro_Liquido_',
					'Divida_Bruta_Lucro_Liquido_']

	def Divida_Bruta_Lucro_Liquido_(self, obj):
		if obj.Divida_Bruta_Lucro_Liquido() is None:
			return 'Sem registo'
		if obj.Divida_Bruta_Lucro_Liquido() == 0:
			return obj.Divida_Bruta_Lucro_Liquido()
		return mark_safe(f'MZN {obj.Divida_Bruta_Lucro_Liquido()}')
	Divida_Bruta_Lucro_Liquido_.short_description = 'Divida Bruta Lucro Liquido'

	def Divida_Liquido_Lucro_Liquido_(self, obj):
		if (obj.Divida_Liquido_Lucro_Liquido() is None or
			obj.Divida_Liquido_Lucro_Liquido() == 0):
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Divida_Liquido_Lucro_Liquido()}')
	Divida_Liquido_Lucro_Liquido_.short_description = 'Divida Liquido Lucro Liquido'

	def Divida_Liquido_EBITDA_(self, obj):
		return obj.Divida_Liquido_EBITDA()
	Divida_Liquido_EBITDA_.short_description = 'Divida Liquido EBITDA'

	def Divida_Liquido_EBITD_(self, obj):
		if (obj.Divida_Liquido_EBITD() is None or
			obj.Divida_Liquido_EBITD() == 0):
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Divida_Liquido_EBITD()}')
	Divida_Liquido_EBITD_.short_description = 'Divida Liquido EBITD'

	def Divida_Patrimonio_Liquido_(self, obj):
		if (obj.Divida_Patrimonio_Liquido() is None or
			obj.Divida_Patrimonio_Liquido() == 0):
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Divida_Patrimonio_Liquido()}')
	Divida_Patrimonio_Liquido_.short_description = 'Divida Patrimonio Liquido'


	def Divida_or_Activo_Total_(self, obj):
		if obj.Divida_or_Activo_Total() is None:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Divida_or_Activo_Total()}')
	Divida_or_Activo_Total_.short_description = 'Divida or Activo Total'

	def Liquidez_Geral_(self, obj):
		if obj.Liquidez_Geral() is None:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Liquidez_Geral()}')
	Liquidez_Geral_.short_description = 'Liquidez Geral'

	def Liquidez_Seca_(self, obj):
		if obj.Liquidez_Seca() is None:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Liquidez_Seca()}')
	Liquidez_Seca_.short_description = 'Liquidez Seca'

	def Liquidez_Corrente_(self, obj):
		if obj.Liquidez_Corrente() is None:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Liquidez_Corrente()}')
	Liquidez_Corrente_.short_description = 'Liquidez Corrente'


@admin.register(IndicadoresDeCrescimento)
class IndicadoresDeCrescimentoAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'CAGR_Receita_5A_',
					'CAGR_Lucro_5A_']

	def CAGR_Receita_5A_(self, obj):
		if obj.CAGR_Receita_5A() is None:
			return mark_safe(f'Sem registo')
		return mark_safe(f'{obj.CAGR_Receita_5A()}%')
	CAGR_Receita_5A_.short_description = 'CAGR Receita 5A'

	def CAGR_Lucro_5A_(self, obj):
		if obj.CAGR_Lucro_5A() is None:
			return mark_safe(f'Sem registo')
		return mark_safe(f'{obj.CAGR_Lucro_5A()}%')
	CAGR_Lucro_5A_.short_description = 'CAGR Lucro 5A'


@admin.register(IndicadoresDeEficiencia)
class IndicadoresDeEficienciaAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'margem_bruta_',
					'margin_EBITIDA_', 'margin_EBIT_',
					'margin_Liquida_']

	def margem_bruta_(self, obj):
		if obj.margem_bruta() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.margem_bruta()}%')
	margem_bruta_.short_description = 'Margem Bruta'

	def margin_EBITIDA_(self, obj):
		return obj.margin_EBITIDA()

	def margin_Liquida_(self, obj):
		if obj.margin_Liquida() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.margin_Liquida()}%')
	margin_Liquida_.short_description = 'Margin Liquida' 

	def margin_EBIT_(self, obj):
		if obj.margin_EBIT() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.margin_EBIT()}%')
	margin_EBIT_.short_description = 'margin EBIT' 


@admin.register(IndicadoresDeRentabilidade)
class IndicadoresDeRentabilidadeAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'ROA_', 
					'ROE_', 'Roic_', 'Giro_dos_Activos']

	def ROA_(self, obj):
		if obj.ROA() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.ROA()}%')
	ROA_.short_description = 'ROA'

	def ROE_(self, obj):
		if obj.ROE() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.ROE()}%')
	ROE_.short_description = 'ROE'

	def Roic_(self, obj):
		if obj.Roic() is None:
			return 'Sem registo'
		return mark_safe(f'{obj.Roic()}%')
	Roic_.short_description = 'Roic'

	def Giro_dos_Activos(self, obj):
		if obj.Giro_dos_Activos() is None:
			return 'Sem registo'
		return mark_safe(f'MZN {obj.Giro_dos_Activos()}')
	Giro_dos_Activos.short_description = 'Giro_dos_Activos'	


@admin.register(DemonstracaoDeFluxoDeCaixa)
class DemonstracaoDeFluxoDeCaixaAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'fundos_gerados_das_actividades_operacionais', 
					'fundos_utilizados_em_actividades_de_investimento', 
					'fundos_introduzidos_atraves_de_actividades_de_financiamento', 
					'acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa',
					'fluxo_de_caixa']

	def fluxo_de_caixa(self, obj):
		return obj.fluxo_de_caixa()
	fluxo_de_caixa.short_description = 'Fluxo de Caixa'

@admin.register(DemonstracaoDeResultados)
class DemonstracaoDeResultadosAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'vendas', 'lucros_bruto', 'EBITIDA', 'EBIT',
					'lucro_antes_de_imposto', 'impostos', 'lucro_liquido_depois_de_imposto', 
					'dividendo_declarados_e_pagos', 'numero_medio_ponderado_de_acoes',
					'lucro_por_acao', 'dividendo_por_acao']

	def impostos(self, obj):
		return obj.impostos()
	impostos.short_description = 'Importos'

	def lucro_por_acao(self, obj):
		return obj.lucro_por_acao()
	lucro_por_acao.short_description = 'Lucro por Acao'

	def dividendo_por_acao(self, obj):
		return obj.dividendo_por_acao()
	dividendo_por_acao.short_description = 'Dividendo por Acao'

@admin.register(TableDeDivida)
class TableDeDividaAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'divida_bruta', 'divida_liquida']

	def ano(self, obj):
		return obj.balanco.ano

	def divida_liquida(self, obj):
		return obj.divida_liquida()
	divida_liquida.short_description = 'Divida Liquida'

	def balanco_(self, obj):
		return obj.balanco
	balanco_.short_description = 'Divida Bruta'


@admin.register(Balanco)
class BalancoAdmin(admin.ModelAdmin):
	list_display = ['id', 'ano', 'activo_corrente', 'caixa', 'inventarios',
					'activo_nao_corrente', 'total_de_activo', 'passivo_corrente',
					'passivo_nao_corrente', 'total_de_passivo', 'capital_social',
					'premio_de_emissao', 'reservas_nao_distribuidas',
					'lucros_acumulados', 'total_do_capital_proprio',
					'total_do_passvo_e_capital_proprio']

	def total_do_passvo_e_capital_proprio(self, obj):
		return obj.total_do_passvo_e_capital_proprio()
	total_do_passvo_e_capital_proprio.short_description = 'Total do Passvo e Capital Proprio'

	def total_do_capital_proprio(self, obj):
		return obj.total_do_capital_proprio()
	total_do_capital_proprio.short_description = 'Total do Capital Proprio'

	def total_de_passivo(self, obj):
		return obj.total_de_passivo()
	total_de_passivo.short_description = 'Total do Passivo'

	def total_de_activo(self, obj):
		return obj.total_de_activo()
	total_de_activo.sort_description = 'Total do Activo'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'first_name', 'last_name',
					'email', 'location']
	list_display_links = ['id', 'user']
	