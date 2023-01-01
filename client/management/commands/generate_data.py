from django.core.management.base import (
	BaseCommand, CommandError
)
from client.models import (
	Balanco, TableDeDivida, DemonstracaoDeResultados,
	DemonstracaoDeFluxoDeCaixa, IndicadoresDeRentabilidade,
	IndicadoresDeEficiencia, IndicadoresDeCrescimento,
	IndicadoresDeEndividamento,
	MetricasPorAccao,
	CotacoesDasAcoes,
	Company,
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



		with open('CotacoesDasAcoes.json') as f:
			data = json.loads(f.read())

		for row in data:
			row = row['fields']
			substitute(row, 'CDM', 1)
			substitute(row, '2Business', 2)
			substitute(row, 'Arco Investimentos', 3)
			substitute(row, 'Arko Seguros', 4)
			substitute(row, 'CMH', 5)
			substitute(row, 'Ceta', 6)
			substitute(row, 'Emose', 7)
			substitute(row, 'Hidroelectrica de Cahora Bassa', 8)
			substitute(row, 'Paytech', 9)
			substitute(row, 'Revimo', 10)
			substitute(row, 'Touch Publicidade', 11)
			substitute(row, 'Zero Investimentos', 12)
			print(row)

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




