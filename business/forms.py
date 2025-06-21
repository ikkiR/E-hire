from django import forms
from django.core.exceptions import ValidationError
from .import models
from datetime import date, timedelta
import re
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    #criando o campo no forms mas sem necessariamente guardar no banco, apenas validar.
    aceitou_termos = forms.BooleanField(
        widget= forms.CheckboxInput(attrs={'id':'termos'}),
        required=False
    )

    confirmar_senha = forms.CharField(
        widget = forms.PasswordInput(attrs={'id': 'confirmPassword', 'placeholder':'Confirme sua senha'}),
        required=False
    )

    class Meta:
        model = models.Empresa
        fields = ('companyName','tradingName','cnpj','stateRegistration','companyEmail','companyPhone','cep','address','number','complement','neighborhood','city','state','country','password',)
        widgets = {
            'companyName': forms.TextInput(attrs={'id':'companyName','placeholder': 'Insira o nome da empresa'}),
            'tradingName': forms.TextInput(attrs={'id':'tradingName','placeholder': 'Insira o nome Fantasia'}),
            'cnpj': forms.TextInput(attrs={'id':'cnpj','placeholder':'Formato: 00.000.000/0000-00'}),
            'stateRegistration': forms.TextInput(attrs={'id':'stateRegistration','placeholder':'Insira a inscrição estadual' }),
            'companyEmail': forms.EmailInput(attrs={'id':'companyEmail','placeholder':'Insira um E-mail'}),
            'companyPhone': forms.TextInput(attrs={'id':'companyPhone','placeholder':'Insira um telefone'}),
            'cep': forms.TextInput(attrs={'id':'cep','placeholder':'Insira um CEP'}),
            'address': forms.TextInput(attrs={'id':'address','placeholder':'Insira um endereço'}),
            'number': forms.TextInput(attrs={'id':'number','placeholder':'Insira um número de endereço'}),
            'complement': forms.TextInput(attrs={'id':'complement','placeholder':'Insira um complemento se houver'}), 
            'neighborhood': forms.TextInput(attrs={'id':'neighborhood','placeholder':'Insira um bairro'}),
            'city': forms.TextInput(attrs={'id':'city','placeholder':'Insira uma cidade'}),
            'state': forms.Select(attrs={'id':'state'}),
            'country':forms.TextInput(attrs={'id':'country','readonly':'readonly'}),
            'password':forms.PasswordInput(attrs={'id': 'password','placeholder':'Insira Uma senha de 8 caracteres'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].initial = 'Brasil'
        for field in ['companyName','tradingName','cnpj','stateRegistration','companyEmail','companyPhone','cep','address','number','complement','neighborhood','city','state','country','password']:
            self.fields[field].required = False


    def clean_cnpj(self):

        cnpj = self.cleaned_data.get('cnpj')

        if not cnpj:
            raise forms.ValidationError("Por favor preencha o campo de CNPJ.")

        # Remove qualquer caractere que não seja número
        cnpj = re.sub(r'[^0-9]', '', cnpj)

        if len(cnpj) != 14:
            raise forms.ValidationError("CNPJ deve conter 14 números.")

        if cnpj in (c * 14 for c in "1234567890"):
            raise forms.ValidationError("CNPJ inválido.")

        def calcula_digito(cnpj, peso):
            soma = sum(int(a) * b for a, b in zip(cnpj, peso))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        peso2 = [6] + peso1

        #faz o calculo dos digitos para validação
        digito1 = calcula_digito(cnpj[:12], peso1)
        digito2 = calcula_digito(cnpj[:12] + digito1, peso2)

        if cnpj[-2:] != digito1 + digito2:
            raise forms.ValidationError("CNPJ inválido.")

        return cnpj


    def clean_stateRegistration(self):
        stateRegistration = self.cleaned_data.get('stateRegistration')

        if not stateRegistration:
            raise forms.ValidationError("Por favor preencha o campo.")


        stateRegistration = re.sub(r'[^0-9]', '', stateRegistration)


        if not stateRegistration.isdigit() or len(stateRegistration) != 12 :
            raise forms.ValidationError("A inscrição deve conter 9 números.")
        
        return stateRegistration
    
    def clean_companyPhone(self):
        companyPhone = self.cleaned_data.get('companyPhone')

        if not companyPhone:
            raise forms.ValidationError("por favor preencha o campo")
        
        if not companyPhone.isdigit():
            raise forms.ValidationError("E campo de telefone deve conter apenas números")
        
        if len(companyPhone) < 11 :
            raise forms.ValidationError("O telefone deve conter 11 números (xx)xxxxxxxxx")

        return companyPhone 

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')

        if not cep:
            raise forms.ValidationError("Por favor preencha este campo.")
        
        cep = re.sub(r'[^0-9]', '', cep)

        if cep in [c * 8 for c in "12345678"]:
            raise forms.ValidationError("CEP inválido.")
        
        if cep == '12345678':
            raise forms.ValidationError('Esse CEP não é valido.')

        if not cep.isdigit():
            raise forms.ValidationError("O Campo de CEP deve conter apenas números")

        if len(cep) < 8:
            raise forms.ValidationError("Um cep deve conter 8 números")            

        return cep
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Verifica o comprimento mínimo
        if len(password) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")

        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")

        # Verifica se contém pelo menos uma letra minúscula
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra minúscula.")

        # Verifica se contém pelo menos um número
        if not re.search(r'\d', password):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")

        # Verifica se contém pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("A senha deve conter pelo menos um caractere especial.")

        return password


    def clean(self):
        cleaned_data= super().clean()

        companyName = cleaned_data.get('companyName')
        tradingName = cleaned_data.get('tradingName')
        password = cleaned_data.get('password')
        address = cleaned_data.get('address')
        companyEmail = cleaned_data.get('companyEmail')
        number = cleaned_data.get('number')
        neighborhood = cleaned_data.get('neighborhood')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        aceitou_termos = cleaned_data.get('aceitou_termos')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if not companyName:
            self.add_error('companyName', 'Por favor, adicione o Nome da empresa.')

        if not companyEmail:
            self.add_error('companyEmail','Por favor Preencha o campo de Email')

        if not address:
            self.add_error('address', 'Por favor, adicione um endereço Válido.')

        if not number:
            self.add_error('number','Por favor, adicione o número de endereço')

        if not number.isdigit():
            self.add_error('number','Nesse campo deve conter apenas números')

        if not neighborhood:
            self.add_error('neighborhood', 'por favor, adicione o Bairro'),

        if not city:
            self.add_error('city', 'Por favor, adicione uma cidade.')
        
        if not state:
            self.add_error('state', 'Por favor, selecione uma opção de estado.')

        if not aceitou_termos:
            self.add_error('aceitou_termos', 'Por favor, leia e aceite os temos antes de confirmar.')

        if not confirmar_senha:
            self.add_error('confirmar_senha', 'Por favor, confirme a senha.')

        if not tradingName:
            cleaned_data['tradingName'] = companyName

        if password and confirmar_senha and password != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem')


        return cleaned_data
    

    def save(self, commit=True):
        empresa = super().save(commit=False)
        empresa.set_password(self.cleaned_data["password"])
        if commit:
            empresa.save()
        return empresa
        
        
class SolitacaoForms(forms.ModelForm):
    class Meta:
        model = models.Servico
        fields = ('titulo', 'descricao_rapida', 'descricao_detalhada', 'preco_estimado', 'categoria', 'prazo_estimado',)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Serviço'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'preco_estimado': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'R$ 0,00'}),
            'prazo_estimado': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'descricao_rapida': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Resuma o serviço em uma frase curta (máx. 100 caracteres)'}),
            'descricao_detalhada': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descreva com detalhes o serviço que você precisa, incluindo requisitos, especificações técnicas e qualquer outra informação relevante.'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['titulo','categoria','preco_estimado','prazo_estimado', 'descricao_rapida', 'descricao_detalhada']:
            self.fields[field].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        titulo = cleaned_data.get('titulo')
        categoria = cleaned_data.get('categoria')
        preco_estimado = cleaned_data.get('preco_estimado')
        prazo_estimado = cleaned_data.get('prazo_estimado')
        descricao_rapida = cleaned_data.get('descricao_rapida')
        descricao_detalhada = cleaned_data.get('descricao_detalhada')

        data_de_hoje = date.today()

        if not titulo:
            self.add_error('titulo', 'Você não deu um titulo a este serviço.')


        if not categoria:
            self.add_error('categoria', 'Você não adicionou uma categoria de serviço')

    
        if not preco_estimado:
            self.add_error('preco_estimado', 'Você não adicinou nenhum valor orçamentário inicial.')
            
        if preco_estimado is None:
                self.add_error('preco_estimado', 'Nenhum valor orçamentário incial.')
    
        if preco_estimado is not None:
            if preco_estimado < 0:
                self.add_error('preco_estimado','O valor orçamentário deve ser maior que zero.')
            if preco_estimado > 0 and preco_estimado < 20:
                self.add_error('preco_estimado', "Valor orçamentário Inicial abaixo do minimo esperado (20R$)")
            
        
        if prazo_estimado is None:
            self.add_error('prazo_estimado', 'Nenhuma data selecionada.')

        if prazo_estimado is not None:
            if prazo_estimado == data_de_hoje:
                self.add_error('prazo_estimado', 'A data selecionada não é valida')

            if prazo_estimado <= data_de_hoje + timedelta(days=9):
                self.add_error('prazo_estimado', 'O prazo Minimo é de 10 dias, por favor adicione outra data')
                

        if not descricao_rapida:
            self.add_error('descricao_rapida', 'Você não deixou uma descrição rápida para este serviço.')

        if descricao_rapida is not None:
            if len(descricao_rapida) < 10:
                self.add_error('descricao_rapida','Adicione mais informações a sua descrição rápida ( minimo 10 caracteres)')

        if not descricao_detalhada:
            self.add_error('descricao_detalhada', 'Você não deixou uma descrição detalhada para este serviço.')
        
        if descricao_detalhada is not None:
            if len(descricao_detalhada) < 20:
                self.add_error('descricao_detalhada','Adicione mais informações a sua descrição rápida ( minimo 20 caracteres)')

        
        return cleaned_data


class LoginForms(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForms, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Insira o E-mail da empresa'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Insira a senha'})

