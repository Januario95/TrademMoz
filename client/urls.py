from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
	register_page, login_page,
	profile,
	logout_page, homepage,
	investiments_analysis, cdn_page,
	papel_commercial,
	only_page,
)

from .api_views import (
	CotacoesDasAcoesModelViewSet
)

# router = DefaultRouter()
# router.register('cotacoes-das-acoes', CotacoesDasAcoesModelViewSet)

app_name = 'client'


urlpatterns = [
	# path('', include(router.urls)),

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


