from django.urls import path
from business import views
from django.contrib.auth import views as auth_views



app_name = 'business'

    #Renderização de páginas
urlpatterns = [
    path('', views.index, name='index'),
    path('FAQ/', views.faq, name='FAQ'),
    path('servicos/', views.servicos, name='servicos'),
    path('servicos/solicitacao/', views.solicitacoes, name='solicitacao'),
    path('servicos/empresas/', views.empresas, name='empresas'),
    path('servicos/creditos/', views.creditos, name='creditos'),
    path('RedefinirSenha/', views.redefinir_senha, name='redefinir_senha'),


    #campos de search
    path('search/solicitacao', views.search_solicitacoes, name='SearchSolicitacao'),
    path('search/empresas', views.search_empresas, name='SearchEmpresas'),


    #Solicitação CRUD
    path('cadastre-se/', views.create_empresa, name='cadastro_empresa'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('solicitacao/create_solicitacao/', views.create_solicitacao, name='nova_solicitacao'),
    path('solicitacao/ver_perfil/', views.update_perfil, name='ver_perfil'),
    

    #redefinição de senha
    # página para solicitar email de recuperação
    # path('RedefinirSenha/', auth_views.PasswordResetView.as_view(template_name='registration/redefinir_senha.html'), name='redefinir_senha'),

    # # página informando que o email foi enviado
    # path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='registration/confirmacao_enviada.html'), name='confirmacao_enviada'),

    #  # link enviado por email (com token)
    # path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'email_de_redefinicao.html'), name='email_de_confimacao'),

    # # página de confirmação final
    # path('redefinir-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='confirmacao.html'), name='confirmarEmail'),


]
