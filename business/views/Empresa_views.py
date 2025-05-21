from django.shortcuts import render

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