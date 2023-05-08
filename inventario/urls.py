from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from rest_framework.routers import SimpleRouter

from .views import (
    PessoaAPIViews,
    PessoaAPIViewsDetail,
    PossePessoaObjetoAPIViews,
    PossePessoaObjetoAPIViewsDetail,
    ArmaAPIViews,
    ArmaAPIViewsDetail,
    CarroAPIViews,
    CarroAPIViewsDetail,
    ComputadorAPIViews,
    ComputadorAPIViewsDetail,
    RegistroArmasAPIViews,
    RegistroArmaAPIViewsDetail,
    CompartilhamentoCarroAPIViews,
    CompartilhamentoCarroAPIViewsDetail,
    PesqueisaPosseObjetoView,
    #PessoaCreate
    )
from django.urls import path
routers = SimpleRouter()
# routers.register('pessoacreate', PessoaCreateViewSet)
urlpatterns = [
    
    path('pessoa/',PessoaAPIViews.as_view(),name='pessoa'),
    #path('pessoacreate/',PessoaCreate.as_view(),name='pessoacreate'),
    path('pessoa/<int:pk>',PessoaAPIViewsDetail.as_view(),name='pessoa'),

    path('pessoaposseobjeto/',PossePessoaObjetoAPIViews.as_view(),name='pessoaposseobjeto'),
    path('pessoaposseobjeto/<int:pk>',PossePessoaObjetoAPIViewsDetail.as_view(),name='pessoaposseobjeto'),
    
    path('pesquisaobjeto/',PesqueisaPosseObjetoView.as_view(),name='pesquisaobjeto'),

    path('carro/',CarroAPIViews.as_view(),name='carro'),
    path('carro/<int:pk>',CarroAPIViewsDetail.as_view(),name='carro'),
    
    path('arma/',ArmaAPIViews.as_view(),name='arma'),
    path('arma/<int:pk>',ArmaAPIViewsDetail.as_view(),name='arma'),
    
    path('computador/',ComputadorAPIViews.as_view(),name='computador'),
    path('computador/<int:pk>',ComputadorAPIViewsDetail.as_view(),name='computador'),
    
    path('registroarma/',RegistroArmasAPIViews.as_view(),name='registroarma'),
    path('registroarma/<int:pk>',RegistroArmaAPIViewsDetail.as_view(),name='registroarma'),

    path('compartilharcarro/',CompartilhamentoCarroAPIViews.as_view(),name='compartilharcarro'),
    path('compartilharcarro/<int:pk>',CompartilhamentoCarroAPIViewsDetail.as_view(),name='compartilharcarro'),

]

