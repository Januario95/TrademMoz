from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
	authenticate, login as auth_login, logout
)
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.decorators import (
	login_required
)
from django.http import HttpResponse, JsonResponse

from .models import (
	Client, 
	CotacoesDasAcoes,
	Company, MetricasPorAccao,
)

from .forms import (
	ClientForm,
	LoginForm,
)

import json
from datetime import datetime


# from .serializers import (
# 	CotacoesDasAcoesSerializer,
# )


# class CotacoesDasAcoesModelViewSet(ModelViewSet):
# 	queryset = CotacoesDasAcoes.objects.all()
# 	serializer_class = CotacoesDasAcoesSerializer


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
 #    titles = [
	# 	{'name': 'CDM', 'img': 'cdm.jpg'}, 
	# 	{'name': 'CMH', 'img': 'cdm.jpg'}, {'name': 'Arko Seguros', 'img': 'cdm.jpg'}, 
	# 	{'name': 'Zero Investimentos', 'img': 'cdm.jpg'}, 
	# 	{'name': '2Business', 'img': 'cdm.jpg'},
	#     {'name': 'Tropigalia', 'img': 'cdm.jpg'}, 
	#     {'name': 'HCB', 'img': 'cdm.jpg'}, {'name': 'Emose', 'img': 'cdm.jpg'},
	#     {'Arko Investimentos', 'cdm.jpg'}, {'Revimo', 'cdm.jpg'},
	#     {'name': 'PayTach', 'img': 'cdm.jpg'}
	# ]

	# if page == 'index':
	# 	page = page.replace(" ", "_")
	# 	return render(request,
	# 				'pages/investiments_analysis.html',
	# 				{'titles': titles,
	# 				'data': data, 'page': page})
	# else:
	page = page.replace(" ", "_")
	# if page == 'index':
	# 	page = 'CDM'
	return render(request,
				f'pages/{page}.html',
				{'titles': titles, 'index': page, 'page': page.replace('_', ' ')})


def only_page(request, page):
	data = {
		'name': request.user.first_name + ' ' + request.user.last_name
	}
	titles = sorted(['CDM', 'CHM', 'Arko Seguros', 'Zero Investimentos', '2Business',
	          'HCB', 'Emose', 'Arco Investimentos', 'Revimo',
	          'Paytech', 'Touch Publicidade'])
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
	# print(f'date = {objs[objs.count()-1]}')
	# metricas = MetricasPorAccao.objects.filter(
	# 	ano=obj.date.year,
	# 	nome_da_empresa=company_name)
	# print(f'metricas = {metricas}')
	var_media_diaria = 0
	var_media_mensal = 0
	min_value = first_obj.preco_da_acao
	max_value = 0
	for val in objs:
		# print(f'date = {val.date}.\tvar_media_diaria = {val.Variacao_Mensal()}')
		if val.preco_da_acao > max_value:
			max_value = val.preco_da_acao

		if val.preco_da_acao < min_value:
			min_value = val.preco_da_acao

		try:
			var_media_diaria += val.Variacao_Diaria()
		except Exception as e:
			pass

		try:
			var_media_mensal += val.Variacao_Mensal()
		except Exception as e:
			pass

	var_media_diaria = round(var_media_diaria / objs.count(), 2) * 100
	var_media_mensal = round(var_media_mensal / objs.count(), 2) * 100
	serialized = obj.serialize()
	serialized['var_media_diaria'] = var_media_diaria
	serialized['var_media_mensal'] = var_media_mensal
	serialized['min_value'] = min_value
	serialized['max_value'] = max_value
	return render(request,
				'pages/only_page.html',
				{'titles': titles, 'index': page, 'page': page.replace('_', ' '),
				 'cotacao': obj, 'serialized': serialized})


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
				print(data)
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
					return redirect('/')
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
				# print('User does not exists')
				# # print(name)
				# print(email)
				# print(phone_number)
				# print(location)
	else:
		form = ClientForm()

	return render(request,
		          'pages/register.html',
		          {'form': form,
		           'user_exists': user_exists})



