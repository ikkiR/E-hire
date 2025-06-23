from django.shortcuts import render, redirect
from business.models import Empresa
from business.models import Servico
from business.models import Avaliacao
from business.models import Categoria
from django.db.models import Q
from django.db.models import Avg
from django.core.paginator import Paginator


def index (request):
    return render(
        request,
        'business/index.html',
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
    return render(
        request,
        'business/servicos.html',
    )



def search_solicitacoes(request):

    search_value = request.GET.get('q', '').strip()

    if search_value == "":
        return redirect ('business:solicitacao')

    empresas = Empresa.objects.all()
    categorias = Categoria.objects.all()
    servicos_disponiveis = Servico.objects.all().order_by('id').filter(Q(titulo__icontains=search_value) | Q(categoria__name__icontains=search_value))

    disponibilidade = request.GET.get('disponibilidade')
    categoria_id = request.GET.get('categoria')

    if disponibilidade in ['DISP', 'IND']:
        servicos_disponiveis = servicos_disponiveis.filter(disponibilidade=disponibilidade)
 

    # Filtra por categoria só se for número válido
    if categoria_id and categoria_id.isdigit():
        servicos_disponiveis = servicos_disponiveis.filter(categoria_id=categoria_id)

    # Filtra disponibilidade somente se for valor esperado
    if disponibilidade in ['disponivel', 'indisponivel']:
        servicos_disponiveis = servicos_disponiveis.filter(disponibilidade=disponibilidade)

    paginator = Paginator(servicos_disponiveis, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'empresas': empresas,
        'servicos_disponiveis': servicos_disponiveis,
    }

    return render(request, 'business/solicitacao.html', context)



def search_empresas(request):

    search_value = request.GET.get('q', '').strip()
    ordenacao = request.GET.get('ordenacao', 'default')

    if search_value == "":
        return redirect ('business:empresas')

    empresas = Empresa.objects.all().order_by('-id').filter(Q(tradingName__icontains=search_value))


    if ordenacao == 'rating-desc':
        empresas = sorted(empresas, key=lambda e: Avaliacao.objects.filter(proposta__empresa_prestadora=e).aggregate(Avg('nota'))['nota__avg'] or 0, reverse=True)
    elif ordenacao == 'rating-asc':
        empresas = sorted(empresas, key=lambda e: Avaliacao.objects.filter(proposta__empresa_prestadora=e).aggregate(Avg('nota'))['nota__avg'] or 0)
    else:
        empresas = empresas.order_by('-id')




    media_avaliacoes = {
        empresa.id: Avaliacao.objects.filter(proposta__empresa_prestadora=empresa).aggregate(Avg('nota'))['nota__avg']
        for empresa in empresas
    }

    paginator = Paginator(empresas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)    

    context ={
        'page_obj': page_obj,
        'empresas': empresas,
        'media_avaliacoes': media_avaliacoes,
    }

    print(media_avaliacoes)
    return render(
        request,
        'business/empresas.html',
        context,
    )




def solicitacoes(request):
    empresas = Empresa.objects.all()
    categorias = Categoria.objects.all()
    servicos_disponiveis = Servico.objects.all().order_by('-id')


    disponibilidade = request.GET.get('disponibilidade')
    categoria_id = request.GET.get('categoria')

    if disponibilidade in ['DISP', 'IND']:
        servicos_disponiveis = servicos_disponiveis.filter(disponibilidade=disponibilidade)
 

    # Filtra por categoria só se for número válido
    if categoria_id and categoria_id.isdigit():
        servicos_disponiveis = servicos_disponiveis.filter(categoria_id=categoria_id)

    # Filtra disponibilidade somente se for valor esperado
    if disponibilidade in ['disponivel', 'indisponivel']:
        servicos_disponiveis = servicos_disponiveis.filter(disponibilidade=disponibilidade)

   

    paginator = Paginator(servicos_disponiveis, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'empresas': empresas,
        'servicos_disponiveis': servicos_disponiveis,
    }

    return render(request, 'business/solicitacao.html', context)


def empresas(request):

    empresas = Empresa.objects.all().order_by('-id')
    ordenacao = request.GET.get('ordenacao', 'default')

    if ordenacao == 'rating-desc':
        empresas = sorted(empresas, key=lambda e: Avaliacao.objects.filter(proposta__empresa_prestadora=e).aggregate(Avg('nota'))['nota__avg'] or 0, reverse=True)
    elif ordenacao == 'rating-asc':
        empresas = sorted(empresas, key=lambda e: Avaliacao.objects.filter(proposta__empresa_prestadora=e).aggregate(Avg('nota'))['nota__avg'] or 0)
    else:
        empresas = empresas.order_by('-id')

    media_avaliacoes = {
        empresa.id: Avaliacao.objects.filter(proposta__empresa_prestadora=empresa).aggregate(Avg('nota'))['nota__avg']
        for empresa in empresas
    }

    paginator = Paginator(empresas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)    

    context ={
        'page_obj': page_obj,
        'empresas': empresas,
        'media_avaliacoes': media_avaliacoes,
    }

    print(media_avaliacoes)
    return render(
        request,
        'business/empresas.html',
        context,
    )


def creditos(request):
    return render(
        request,
        'business/credito.html',
    )