from django.urls import path
from business import views



app_name = 'business'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastre-se/', views.cadastro_empresa, name='cadastro_empresa'),
    path('FAQ/', views.faq, name='FAQ'),
    path('RedefinirSenha/', views.redefinir_senha, name='RedefinirSenha'),
]
