from django import forms
from django.contrib.auth.models import User

from .models import (
	Client, CotacoesDasAcoes,
)


class CotacoesDasAcoesForm(forms.ModelForm):
	# date = forms.DateField()
	
	class Meta:
		model = CotacoesDasAcoes
		fields = '__all__'
		

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255)
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput)

	# class Meta:
	# 	model = User
	# 	fields = ('username', 'password')


class ClientForm(forms.Form):
	username = forms.CharField(
		max_length=255,
		widget=forms.TextInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira nome de usuario aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira o seu email aqui')"
		}))
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira a sua senha aqui')"
		}))
	confirm_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira a sua senha aqui')"
		}))
	phone_number = forms.CharField(
		max_length=50,
		widget=forms.TextInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira o seu numero de telefone')"
		}))
	location = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor insira a sua morada aqui')"
		}))

	# class Meta:
	# 	model = Client
	# 	fields = '__all__'


