from django.shortcuts import render
from business.models import Empresa
from business.models import Proposta



def index (request):
    return render(
        request,
        'business/index.html',
    )


def login (request):
    return render(
        request,
        'business/login.html',
    )


def cadastro_empresa (request):
    return render(
        request,
        'business/cadastro_empresas.html',
    )


def faq (request):
    return render(
        request,
        'business/FAQ.html',
    )


def redefinir_senha (request):
    return render(
        request,
        'business/redefinir_senha.html',
    )


def servicos (request):

    empresas = Empresa.objects.all()
    propostas_disponiveis = Proposta.objects.filter(empresa_prestadora__isnull=True)

    context = {
        'empresas' : empresas,
        'propostas_disponiveis' : propostas_disponiveis,
    }

    return render(
        request,
        'business/servicos.html',
        context,
    )