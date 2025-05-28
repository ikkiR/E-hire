from django.shortcuts import render
from business.models import Empresa
from business.models import Proposta
from business.models import Avaliacao
from django.db.models import Avg
from django.core.paginator import Paginator

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
    media_avaliacoes = {
        empresa.id: Avaliacao.objects.filter(proposta__empresa_prestadora=empresa).aggregate(Avg('nota'))['nota__avg']
        for empresa in empresas
    }

    paginator = Paginator(empresas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj' : page_obj,
        'propostas_disponiveis' : propostas_disponiveis,
        'media_avaliacoes' : media_avaliacoes,
    
    }

    return render(
        request,
        'business/servicos.html',
        context,
    )