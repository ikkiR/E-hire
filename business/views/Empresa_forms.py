from django.shortcuts import render , redirect 
from business.forms import SolitacaoForms
from business.forms import RegisterForm
from business.forms import LoginForms
from business.models import Empresa
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth




def create_empresa(request):
 
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Empresa Registrada')
            return redirect('business:login')


    return render(
        request,
        'business/cadastro_empresas.html',
        {
            'form': form
        }
    )




def create_solicitacao (request):
        
    if request.method == 'POST':
        form = SolitacaoForms(request.POST)

        context = {
            'form' : form
        
        }

        if form.is_valid():
            form.save()
            return redirect('business:solicitacao')


        return render(
            request,
            'business/create_solicitacao.html',
            context,
        )

    context = {
        'form' : SolitacaoForms()
    }

    return render(
        request,
        'business/create_solicitacao.html',
        context,
    )


def login (request):

    if request.method == 'POST':
        form = LoginForms(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Usuário Logado com sucesso")
            return redirect('business:servicos')
        messages.error(request, "Login inválido")
    else:
        form = LoginForms(request)


    return render(
        request,
        'business/login.html',
        {
            'form':form,
        }
    )


def logout_view (request):
    auth.logout(request)
    return redirect('business:login')