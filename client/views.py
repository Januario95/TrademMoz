from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
	authenticate, login as auth_login, logout
)
from django.contrib.auth.decorators import (
	login_required
)
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse, JsonResponse

from .models import (
	Client, 
	CotacoesDasAcoes,
	Company, MetricasPorAccao,
	DemonstracaoDeResultados,
	IndicadoresDeRentabilidade,
)

from .forms import (
	ClientForm,
	LoginForm,
	CotacoesDasAcoesForm,
)

import json
from datetime import datetime, timedelta


# from .serializers import (
# 	CotacoesDasAcoesSerializer,
# )


def get_compay_names_and_ids(request):
	companies = Company.objects.all()
	companies_ = []
	for company in companies:
		company = company.name.replace(' ', '-').replace('_', '-').lower()[::-1]
		companies_.append(company)

	return JsonResponse({
		'companies': companies_
	})


@login_required
def papel_commercial(request):
	return render(request,
				  'pages/papel_comercial.html',
				  {'user': request.user})


@login_required
def profile(request):
	return render(request,
				  'pages/profile.html',
				  {'user': request.user})

def cdn_page(request):
	return render(request,
				  'pages/cdn_page.html',
				  {'text': 'CDN Page'})


def investiments_analysis(request, page='CDM'):
	data = {
		'name': request.user.first_name + ' ' + request.user.last_name
	}
	titles = ['CDM', 'CMH', 'Arko Seguros', 'Zero Investimentos', '2Business',
	          'Tropigalia', 'HCB', 'Emose', 'Arko Investimentos', 'Revimo',
	          'PayTach']

	page = page.replace(" ", "_")
	return render(request,
				f'pages/{page}.html',
				{'titles': titles, 'index': page, 'page': page.replace('_', ' ')})


def get_cotacao(request, pk):
	cotacao = CotacoesDasAcoes.objects.filter(pk=pk)
	if cotacao.exists():
		cotacao = cotacao.first().serialize()
	else:
		cotacao = {}

	return JsonResponse({
		'cotacao': cotacao
	})

def delete_cotacao(request, pk):
	cotacao = CotacoesDasAcoes.objects.filter(pk=pk)
	deleted = False
	if cotacao.exists():
		cotacao = cotacao.first()
		cotacao.delete()
		deleted = True

	return JsonResponse({
		'deleted': deleted
	})

def get_cotacoes(company_name):
	company = Company.objects.filter(name=company_name)
	if company.exists():
		company = company.first()
		cotacoes = CotacoesDasAcoes.objects.filter(
			nome_da_empresa=company)
	else:
		cotacoes = {}
	return cotacoes

def update_company(request, company_name):
	# company = Company.objects.filter(name=company_name)
	# if company.exists():
	# 	company = company.first()
	# 	cotacoes = CotacoesDasAcoes.objects.filter(
	# 		nome_da_empresa=company)
	# else:
	# 	cotacoes = {}
	cotacoes = get_cotacoes(company_name)
	titles_ = Company.objects.all()
	titles = []
	for title in titles_:
		titles.append(title.name)

	# titles = sorted(['CDM', 'CMH', 'Arko Seguros', 'Zero Investimentos', '2Business',
	#           'HCB', 'Emose', 'Arco Investimentos', 'Revimo',
	#           'Paytech', 'Touch Publicidade'])

	if cotacoes:
		ultima_cotacao = cotacoes.last()
		data_da_ultima_cotacao = ultima_cotacao.date + timedelta(days=1)
		cotacoes = cotacoes.order_by('-date')
	else:
		data_da_ultima_cotacao = ''

	if request.method == 'POST':
		form = CotacoesDasAcoesForm(request.POST)
		if form.is_valid():
			# form.save()
			data = form.cleaned_data
			print(data)
			# date = data['date']
			# nome_da_empresa = data['nome_da_empresa']
			# preco_da_acao = data['preco_da_acao']
			# cotacoes = get_cotacoes(company_name)
		else:
			print(form.errors)
	else:
		form = CotacoesDasAcoesForm(initial={
			'date': data_da_ultima_cotacao,
			'nome_da_empresa': Company.objects.get(name='CDM'),
			'preco_da_acao': 70
		})

	return render(request,
				'pages/update_company.html',
				{'user': request.user, 'titles': titles,
				 'cotacoes': cotacoes, 'form': form})

def get_color_by_value(value):
	if value < 0:
		color = 'bg-red'
	else:
		color = 'bg-green'
	return color

def get_value_and_color(variable):
	row = {}
	row['value'] = variable
	row['color'] = get_color_by_value(variable)
	return row

def only_page(request, page):
	data = {
		'name': request.user.first_name + ' ' + request.user.last_name
	}
	titles_ = Company.objects.all()
	titles = []
	for title in titles_:
		titles.append(title.name)

	company_name = page
	if company_name == 'HCB':
		company_name = 'Hidroelectrica de Cahora Bassa'
	page = page.replace(" ", "_")
	company = Company.objects.get(name=company_name)
	objs = CotacoesDasAcoes.objects.filter(
		nome_da_empresa=company
	)
	first_obj = objs.first()
	obj = objs.last()
	serialized = obj.serialize()

	min_value = first_obj.preco_da_acao
	max_value = 0

	dividendo_por_acao_ultimo_valor = None
	P_L = None
	
	try:
		LPA = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		LPA = LPA.LPA()
		serialized['LPA'] = get_value_and_color(LPA)
	except Exception as e:
		pass

	try:
		Dividend_Yield = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		Dividend_Yield = Dividend_Yield.Dividend_Yield()
		# serialized['Dividend_Yield'] = Dividend_Yield
		serialized['Dividend_Yield'] = get_value_and_color(Dividend_Yield)
	except Exception as e:
		pass

	
	try:
		P_EBIT = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		P_EBIT = P_EBIT.P_EBIT()
		# serialized['P_EBIT'] = P_EBIT
		serialized['P_EBIT'] = get_value_and_color(P_EBIT)
	except Exception as e:
		pass

	try:
		P_VPA = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		P_VPA = P_VPA.P_VPA()
		serialized['VPL'] = get_value_and_color(P_VPA)
	except Exception as e:
		pass

	try:
		VPL_ = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		VPL = VPL_.VPL()
	except Exception as e:
		pass


	try:
		Valor_Do_Mercado = obj.Valor_Do_Mercado()
		serialized['Valor_Do_Mercado'] = get_value_and_color(Valor_Do_Mercado)
	except Exception as e:
		pass

	try:
		EV_EBIT = obj.EV_EBIT()
		serialized['EV_EBIT'] = get_value_and_color(EV_EBIT)
	except Exception as e:
		pass

	try:
		ebit = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		EBIT_ACTOVOS = ebit.EBIT_ACTOVOS()
		serialized['EBIT_ACTOVOS'] = get_value_and_color(EBIT_ACTOVOS)
	except Exception as e:
		pass


	try:
		VPL_Nas_Acoes = VPL_.VPL_Nas_Acoes(page.replace('_', ' '))
		serialized['VPL_Nas_Acoes'] = get_value_and_color(VPL_Nas_Acoes)
	except Exception as e:
		pass

	try:
		P_ACTIVO = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		P_ACTIVO = P_ACTIVO.P_ACTIVO()
		serialized['P_ACTIVO'] = get_value_and_color(P_ACTIVO)
	except Exception as e:
		pass

	try:
		PSR = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		PSR = PSR.PSR()
		serialized['PSR'] = get_value_and_color(PSR)
	except Exception as e:
		pass

	try:
		P_Capital_De_Giro = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		P_Capital_De_Giro = P_Capital_De_Giro.P_Capital_De_Giro()
		serialized['P_Capital_De_Giro'] = get_value_and_color(P_Capital_De_Giro)
	except Exception as e:
		pass

	try:
		P_Capital_De_Giro_Liquido = MetricasPorAccao.objects.filter(
			nome_da_empresa=company).first()
		P_Capital_De_Giro_Liquido = P_Capital_De_Giro_Liquido.P_Capital_De_Giro_Liquido()
		serialized['P_Capital_De_Giro_Liquido'] = get_value_and_color(P_Capital_De_Giro_Liquido)
	except Exception as e:
		pass
	
	Indicadores = IndicadoresDeRentabilidade.objects.filter(
		nome_da_empresa=company
	)
	ROE = 0.0
	if Indicadores.exists():
		Indicadores = Indicadores.last()
		print(f'LAST YEAR = {Indicadores.ano}')
		ROE = Indicadores.ROE()
		print(f'ROE = {ROE}')
		serialized['ROE'] = get_value_and_color(ROE)

		Roic = Indicadores.Roic()
		print(f'Roic = {Roic}')
		serialized['Roic'] = get_value_and_color(Roic)

		ROA = Indicadores.ROA()
		print(f'ROA = {ROA}')
		serialized['ROA'] = get_value_and_color(ROA)

		Giro_dos_Activos = Indicadores.Giro_dos_Activos()
		print(f'Giro_dos_Activos = {Giro_dos_Activos}')
		serialized['Giro_dos_Activos'] = get_value_and_color(Giro_dos_Activos)

	index_counter_for_semanal = 0
	index_counter_for_mensal = 0
	var_media_diaria = 0
	var_media_semanal = 0
	var_media_mensal = 0
	for val in objs:
		P_L = val.P_L()
		dividendo_por_acao_ultimo_valor = val.dividendo_por_acao_ultimo_valor(company)

		if val.preco_da_acao > max_value:
			max_value = val.preco_da_acao

		if val.preco_da_acao < min_value:
			min_value = val.preco_da_acao

		try:
			var_media_diaria += val.Variacao_Diaria()
		except Exception as e:
			pass

		try:
			var_media_semanal += val.Variacao_Semanal()
			index_counter_for_semanal += 1
		except Exception as e:
			pass

		try:
			var_media_mensal += val.Variacao_Mensal()
			index_counter_for_mensal += 1
		except Exception as e:
			pass

	var_media_diaria = round(var_media_diaria / objs.count(), 2)
	var_media_mensal = round(var_media_mensal / index_counter_for_mensal, 2)
	var_media_semanal = round(var_media_semanal / index_counter_for_semanal, 2)
	
	serialized['var_media_diaria'] = get_value_and_color(var_media_diaria)
	serialized['var_media_semanal'] = get_value_and_color(var_media_semanal)
	serialized['var_media_mensal'] = get_value_and_color(var_media_mensal)
	serialized['min_value'] = get_value_and_color(min_value)
	serialized['max_value'] = get_value_and_color(max_value)
	try:
		serialized['dividendo_por_acao_ultimo_valor'] = get_value_and_color(dividendo_por_acao_ultimo_valor)
	except Exception as e:
		pass

	try:
		serialized['P_L'] = get_value_and_color(P_L)
	except Exception as e:
		pass

	last_date = CotacoesDasAcoes.objects.last()
	today = last_date.date
	return render(request,
				'pages/only_page.html',
				{'titles': titles, 'index': page, 'page': page.replace('_', ' '),
				 'cotacao': obj, 'serialized': serialized, 'today': today})


@login_required
def homepage(request):
	data = {
		'name': request.user.first_name + ' ' + request.user.last_name
	}
	return render(request,
				  'pages/homepage.html',
				  {'data': data})


def logout_page(request):
	logout(request)
	return redirect('/login/')


def login_page(request):
	message = None
	if request.user.is_authenticated:
		return redirect('/')
	else:
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				username = data['username']
				password = data['password']
				user = authenticate(
					request,
					username=username,
					password=password
				)
				print(user)
				if user is not None:
					auth_login(request, user)
					return redirect('/only_page/CDM/')
				else:
					message = 'Wrong username or password'
		else:
			form = LoginForm()

	return render(request,
				  'pages/login.html',
				  {'form': form,
				   'message': message})



def register_page(request):
	user_exists = None
	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			username, first_name, last_name, email, password, confirm_password, phone_number, location = data.values()
			user = User.objects.filter(
				username=username,
				email=email
			)
			print('PASSWORD=', confirm_password)
			if user.exists():
				user_exists = 'Ja existe um usuario com este email. Cadastre-se com email diferente'
				print(user.first())

			else:
				user = User.objects.create(
					username=username,
					email=email,
					first_name=first_name,
					last_name=last_name
				)
				user.set_password(confirm_password)
				user.save()
				client = Client.objects.create(
					first_name=first_name,
					last_name=last_name,
					user=user,
					email=email,
					phone_number=phone_number,
					location=location
				)
				client.save()
				return redirect('/')
	else:
		form = ClientForm()

	return render(request,
		          'pages/register.html',
		          {'form': form,
		           'user_exists': user_exists})



