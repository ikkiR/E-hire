from django.shortcuts import render , redirect 
from business.forms import SolitacaoForms
from business.forms import RegisterForm
from business.forms import LoginForms
from business.forms import RegisterUpdateForm
from business.models import Empresa
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required




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



@login_required(login_url='business:login')
def create_solicitacao(request):
    if request.method == 'POST':
        form = SolitacaoForms(request.POST)

        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.empresa = request.user  # aqui associa a empresa logada
            solicitacao.save()
            return redirect('business:solicitacao')

        context = {
            'form': form
        }
        return render(
            request,
            'business/create_solicitacao.html',
            context,
        )

    context = {
        'form': SolitacaoForms()
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

@login_required(login_url='business:login')
def logout_view (request):
    auth.logout(request)
    return redirect('business:login')

@login_required(login_url='business:login')
def update_perfil(request):
    if request.method == 'POST':
        form = RegisterUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            empresa = form.save()
            password = form.cleaned_data.get('password')
            if password:
                auth.login(request, empresa)
            return redirect('business:ver_perfil')
        else:
            # Se o form não é válido, mostra com os campos habilitados para correção
            return render(request, 'business/perfil.html', {'form': form})
    
    # No GET, mostra o form com campos desabilitados
    form = RegisterUpdateForm(instance=request.user, disabled=True)
    return render(request, 'business/perfil.html', {'form': form})