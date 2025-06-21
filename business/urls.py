from django.urls import path
from business import views



app_name = 'business'

    #Renderização de páginas
urlpatterns = [
    path('', views.index, name='index'),
    path('FAQ/', views.faq, name='FAQ'),
    path('RedefinirSenha/', views.redefinir_senha, name='RedefinirSenha'),
    path('servicos/', views.servicos, name='servicos'),
    path('servicos/solicitacao/', views.solicitacoes, name='solicitacao'),
    path('servicos/empresas/', views.empresas, name='empresas'),

    #campos de search
    path('search/solicitacao', views.search_solicitacoes, name='SearchSolicitacao'),
    path('search/empresas', views.search_empresas, name='SearchEmpresas'),


    #Solicitação CRUD
    path('solicitacao/create_solicitacao/', views.create_solicitacao, name='nova_solicitacao'),
    path('cadastre-se/', views.create_empresa, name='cadastro_empresa'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    

]
