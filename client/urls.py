from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
	register_page, login_page,
	profile,
	logout_page, homepage,
	investiments_analysis, cdn_page,
	papel_commercial,
	only_page, update_company,
	delete_cotacao, get_cotacao,
	get_compay_names_and_ids,
)

from .api_views import (
	CotacoesDasAcoesModelViewSet
)

# router = DefaultRouter()
# router.register('cotacoes-das-acoes', CotacoesDasAcoesModelViewSet)

app_name = 'client'


urlpatterns = [
	# path('', include(router.urls)),

	path('get_compay_names_and_ids/',
		 get_compay_names_and_ids),
	path('get_cotacao/<int:pk>/', get_cotacao),
	path('delete_cotacao/<int:pk>/', delete_cotacao,
		 name='delete_cotacao'),
	path('update_company/<str:company_name>/', 
		 update_company, name='update_company'),
	path('only_page/<str:page>/', only_page, name='only_page'),
	path('papel_commercial/', papel_commercial,
		 name='papel_commercial'),
	path('cdn_page/', cdn_page, name='cdn_page'),
	path('', homepage, name='homepage'),
	path('analise-de-investiments/<str:page>/', investiments_analysis,
		 name='investiments_analysis'),

	path('perfil/', profile, name='profile'),
	path('register/', register_page, name='register'),
	path('login/', login_page, name='login'),
	path('logout/', logout_page, name='logout'),
]




