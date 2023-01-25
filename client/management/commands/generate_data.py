from django.core.management.base import (
	BaseCommand, CommandError
)
from client.models import (
	Balanco, TableDeDivida, DemonstracaoDeResultados,
	DemonstracaoDeFluxoDeCaixa,
	IndicadoresDeEficiencia, IndicadoresDeCrescimento,
	IndicadoresDeEndividamento,
	MetricasPorAccao,
	CotacoesDasAcoes,
	Company,
	IndicadoresDeRentabilidade,
)

import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime


# def generate(data, year):
# 	obj = Balanco.objects.create(
# 		ano=year,
# 		activo_corrente=data[0],
# 		caixa=data[1],
# 		inventarios=data[2],
# 		activo_nao_corrente=data[3],
# 		passivo_corrente=data[4],
# 		passivo_nao_corrente=data[5],
# 		capital_social=data[6],
# 		premio_de_emissao=data[7],
# 		reservas_nao_distribuidas=data[8],
# 		lucros_acumulados=data[9]
# 	)
# 	obj.save()


# def generate(data, year):
# 	obj = DemonstracaoDeFluxoDeCaixa.objects.create(
# 		ano=year,
# 		fundos_gerados_das_actividades_operacionais=data[0],
# 		fundos_utilizados_em_actividades_de_investimento=data[1],
# 		fundos_introduzidos_atraves_de_actividades_de_financiamento=data[2],
# 		acrescimo_ou_decrescimo_em_caixa_e_equivalentes_de_caixa=data[3]
# 	)
# 	obj.save()

def generate(year):
	obj = MetricasPorAccao.objects.create(
		ano=year)
	obj.save()


class Command(BaseCommand):
	help = 'Generate data for Balanco model'

	def handle(self, *args, **options):
		company = Company.objects.get(
			name='Arco Investimentos')
		for year in range(2015, 2021):
			obj = IndicadoresDeEndividamento.objects.create(
				ano=year,
				nome_da_empresa=company
			)
			obj.save()


		# objs = IndicadoresDeCrescimento.objects.all()
		# for obj in objs:
		# 	# obj.nome_da_empresa = company
		# 	# obj.save()
		# 	print(obj)


		# company = Company.objects.get(name='Arco Investimentos')
		# for year in range(2016, 2021):
		# 	obj = IndicadoresDeRentabilidade.objects.create(
		# 		ano=year,
		# 		nome_da_empresa=company
		# 	)
		# 	obj.save()


		# df = pd.read_excel('Demonstracoes-Arco-Inve.xlsx')
		# # print(df.head(2))
		# df = df.T
		# # print(df)

		# columns = [
		# 		'vendas', 'EBITIDA', 'EBIT', 'lucro_antes_de_imposto',
		# 		'impostos', 'lucro_liquido_depois_de_imposto',
		# 		'dividendo_declarados_e_pagos', 'numero_medio_ponderado_de_acoes',
		# 		'ano', 'nome_da_empresa'
 	# 	]
		# year = 2015
		# for row in df.iterrows():
		# 	row = row[1].tolist()
		# 	row.append(year)
		# 	row.append('Arco Investimentos')
		# 	# print(len(columns))
		# 	# print(len(row))
		# 	val = dict(zip(columns, row))
		# 	company = Company.objects.get(name=val['nome_da_empresa'])
		# 	val['nome_da_empresa'] = company
		# 	del val['impostos']
		# 	print(val)
		# 	year += 1

		# 	obj = DemonstracaoDeResultados.objects.create(**val)
		# 	obj.save()


		# values = [6408.081, 951.7, 870.32, 614.424, 668.246, 831.64]
		# years = [2015, 2016, 2017, 2018, 2019, 2020]
		# company = Company.objects.get(name='Arco Investimentos')
		# for year, value in zip(years, values):
		# 	obj = TableDeDivida.objects.create(
		# 		ano=year,
		# 		divida_bruta=value,
		# 		nome_da_empresa=company
		# 	)
		# 	obj.save()


		# df = pd.read_excel('Demonstracoes-Arco-Inve.xlsx')
		# df = df.T.iloc[1:, :]
		# # df = df.iloc[:, :-3]
		# # columns = df.columns.tolist()[1:-1]
		# columns = [
		# 	'activo_corrente', 'caixa', 'inventarios', 'activo_nao_corrente',
		# 	'passivo_corrente', 'passivo_nao_corrente', 'capital_social',
		# 	'premio_de_emissao', 'resultados_transitado', 'resultados_de_exercicio',
		# 	'reservas_nao_distribuidas', 'lucros_acumulados', 'ano', 'nome_da_empresa'
		# ]
		# print(columns)
		# df = df.T

		# year = 2015
		# for row in df.iterrows():
		# 	row = row[1].tolist() # [1:-1]
		# 	row.append(year)
		# 	row.append('Arco Investimentos')
		# 	val = dict(zip(columns, row))
		# 	company = Company.objects.get(name=val['nome_da_empresa'])
		# 	val['nome_da_empresa'] = company
		# 	print(val)
		# 	# obj = Balanco.objects.create(**val)
		# 	# obj.save()
		# 	year += 1



		# company=Company.objects.get(
		# 		name='Hidroelectrica de Cahora Bassa')
		# years = list(range(2014, 2022))
		# for year in years:
		# 	obj = IndicadoresDeRentabilidade.objects.create(
		# 		ano=year,
		# 		nome_da_empresa=company
		# 	)
		# 	obj.save()



		# objs = IndicadoresDeRentabilidade.objects.all()
		# company=Company.objects.get(
		# 		name='CDM')
		# print(company)
		# for obj in objs:
		# 	obj.nome_da_empresa = company
		# 	obj.save()
		# 	print(obj)


		# print(objs.count())
		# years = list(range(2003, 2022))
		# index = 0
		# for obj in objs:
		# 	obj.ano = years[index]
		# 	obj.save()
		# 	print(f'{obj.ano} - {obj.divida_bruta}')
		# 	index += 1


		# df = pd.read_excel('TableDeDivida.xlsx')
		# for row in df.iterrows():
		# 	print(row[0])
		# 	print(row[1].tolist())
		# years = "2014	2015	2016	2017	2018	2019	2020	2021".split("	")
		# years = list(map(int, years))
		# values = "MZN 3,737,181.00	MZN 5,182,544.00	MZN 7,440,874.00	MZN 7,196,150.00	MZN 9,593,970.00	MZN 9,988,132.00	MZN 11,835,385.00	MZN 19,313,958.00".split("MZN ")
		# values = [row.replace('\t', '') for row in values]
		# values = [float(row.replace(',', '')) for row in values if row != '']
		# objs = DemonstracaoDeResultados.objects.filter(
		# 	nome_da_empresa=Company.objects.get(
		# 		name='Hidroelectrica de Cahora Bassa'))
		# index = 0
		# for obj in objs:
		# 	obj.EBIT = values[index]
		# 	obj.save()
		# 	index += 1


		# for year, value in zip(years, values):
		# 	row = {}
		# 	row['ano'] = year
		# 	row['nome_da_empresa'] = Company.objects.get(
		# 		name='Hidroelectrica de Cahora Bassa')
		# 	row['divida_bruta'] = value
		# 	print(row)

			# obj = TableDeDivida.objects.create(**row)
			# obj.save()



		# for year in range(2014, 2022):
		# 	obj = MetricasPorAccao.objects.create(
		# 		ano=str(year),
		# 		nome_da_empresa=Company.objects.get(
		# 			name='Hidroelectrica de Cahora Bassa')
		# 	)
		# 	obj.save()
		# 	print(year)

		# for obj in objs:
		# 	year = obj.ano.split('.')[0]
		# 	obj.ano = int(year)
		# 	obj.save()

		# df = pd.read_excel('Demonstracao_de_Resultados.xlsx')
		# columns = df.columns.tolist()
		# # columns = [col.replace(' ', '_').lower() for col in columns]
		# print(columns)

		# for row in df.iterrows():
		# 	# print(row[1])
		# 	values = row[1].tolist()
		# 	row = dict(zip(columns, values))
		# 	print(row)
		# 	company = Company.objects.get(
		# 		name='Hidroelectrica de Cahora Bassa'
		# 	)

		# 	print(company)
		# 	ano = row['ano']
		# 	vendas = row['vendas']
		# 	lucros_bruto = row['lucros_bruto']
		# 	ebit = row['ebit']
		# 	lucros_de_exploracao = row['lucros_de_exploracao']
		# 	lucro_antes_de_impostos = row['lucro_antes_de_impostos']
		# 	lucro_líquido_depois_de_impostos = row['lucro_líquido_depois_de_impostos']
		# 	dividendos_declarados_e_pagos = row['dividendos_declarados_e_pagos']
		# 	número_médio_ponderado_de_acções = row['número_médio_ponderado_de_acções']

		# 	# row['nome_da_empresa'] = company
		# 	# print(row)

		# 	obj = DemonstracaoDeResultados.objects.create(
		# 		ano=ano,
		# 		nome_da_empresa=company,
		# 		vendas=vendas,
		# 		lucros_bruto=lucros_bruto,
		# 		EBITIDA=ebit,
		# 		EBIT=ebit,
		# 		lucro_antes_de_imposto=lucro_antes_de_impostos,
		# 		lucro_liquido_depois_de_imposto=lucro_líquido_depois_de_impostos,
		# 		dividendo_declarados_e_pagos=dividendos_declarados_e_pagos,
		# 		numero_medio_ponderado_de_acoes=número_médio_ponderado_de_acções
		# 	)
		# 	obj.save()

			# val2 = list(row[1].__dict__.values())[1] # ['Items'] # .tolist()
			# print(type(val2))
			# row_ = dict(zip(val2, values))
			# row_['ano'] = row[0]
			# print(row_)
			# print()



		# objs = Balanco.objects.all()
		# for obj in objs:
		# 	print(obj.ano)

		# url = 'http://localhost:8000/add_new_cotacoes/'

		# print('Paytech')
		# df = pd.read_excel('Paytech.xlsx')
		# print(df.head())

		# for val in df.iterrows():
		# 	row = val[1].values.tolist()
		# 	# res = requests.post(url, data=json.dumps({'data': row}))
		# 	# print(res.json())

		# 	amount = row[1] if row[1] != 'nan' else 0

		# 	row = {
		# 		'date': datetime.strptime(row[0], '%d-%b-%y'),
		# 		'preco_da_acao': amount,
		# 		'nome_da_empresa': row[2]
		# 	}
		# 	print(row)


		# 	obj = CotacoesDasAcoes.objects.filter(
  #   			date=row['date'],
  #   			nome_da_empresa=row['nome_da_empresa']
  #   		)
		# 	# print(obj.exists())
		# 	if obj.exists():
		# 		print('Object exists')
		# 	else:
		# 		print('Object does not exist')
		# 		obj = CotacoesDasAcoes.objects.create(
		# 			**row
		# 		)
		# 		obj.save()
		# 		print(obj)



		# for year in range(2003, 2022):
		# 	generate(year)

		def substitute(row, company_name, id_):
			if row['nome_da_empresa'] == company_name:
				obj = Company.objects.get(id=id_)
				row['nome_da_empresa'] = obj
			return row



		# with open('CotacoesDasAcoes.json') as f:
		# 	data = json.loads(f.read())

		# for row in data:
		# 	row = row['fields']
		# 	substitute(row, 'CDM', 1)
		# 	substitute(row, '2Business', 2)
		# 	substitute(row, 'Arco Investimentos', 3)
		# 	substitute(row, 'Arko Seguros', 4)
		# 	substitute(row, 'CMH', 5)
		# 	substitute(row, 'Ceta', 6)
		# 	substitute(row, 'Emose', 7)
		# 	substitute(row, 'Hidroelectrica de Cahora Bassa', 8)
		# 	substitute(row, 'Paytech', 9)
		# 	substitute(row, 'Revimo', 10)
		# 	substitute(row, 'Touch Publicidade', 11)
		# 	substitute(row, 'Zero Investimentos', 12)
		# 	print(row)

			# try:
			# 	obj = CotacoesDasAcoes.objects.create(**row)
			# 	obj.save()
			# 	print(obj)
			# except Exception as e:
			# 	print(e)
			
			# print(row['fields'])

		# year = 2003
		# row = []
		# for key, value in data.items():
		# 	value = list(value.values())
		# 	# row.append(year)
		# 	# row.extend(value)
		# 	# value.append(year)
		# 	# print(row)
		# 	# row.clear()
		# 	try:
		# 		generate(value, year)
		# 		year += 1
		# 	except Exception as e:
		# 		print(e)
		
		# for obj, divida_bruta in zip(objs, data):
		# 	try:
		# 		generate(obj, data[divida_bruta]['Divida Bruta'])
		# 	except Exception as e:
		# 		print(e)

		# for key, value in data.items():
		# 	value = list(value.values())
		# 	try:
		# 		generate(value, key)
		# 	except Exception as e:
		# 		print(e)

		self.stdout.write(self.style.SUCCESS('Successfully generated data.'))




