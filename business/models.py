from django.db import models
from django.utils import timezone
from datetime import date

class Categoria (models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'

class Empresa (models.Model):
    companyName = models.CharField(max_length=250)
    tradingName = models.CharField(max_length=250, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    stateRegistration = models.CharField(max_length=30, blank=True, null=True)
    companyEmail = models.EmailField()
    companyPhone = models.CharField(max_length=20)
    cep = models.CharField(max_length=9)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    create_date = models.DateTimeField(default=timezone.now)
    sobre = models.TextField(max_length=500, null=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    def __str__(self) -> str:
        return f'{self.tradingName}'



class Servico (models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField()
    preco_estimado = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)
    prazo_estimado = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.titulo}'


class Proposta (models.Model):

    status = [
        ('PD', 'Pendente'),
        ('AC', 'Aceita'),
        ('RC', 'Recusada'),
        ('FN', 'Finalizada'),
    ]

    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True)
    empresa_contratante = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, related_name='propostas_contratadas')
    empresa_prestadora = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, related_name='propostas_prestadas', blank=True)
    data_proposta = models.DateField(default=date.today)
    status = models.CharField(max_length=2, choices=status)
    valor_negociado = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    prazo_negociado = models.CharField(max_length=50, blank=True, null=True)
    descricao_proposta = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        prestadora = self.empresa_prestadora.tradingName if self.empresa_prestadora else "Aguardando"
        return f"{self.servico.titulo} - {self.empresa_contratante.tradingName} x {prestadora}" 


class Avaliacao (models.Model):

    Nota = [
        (1, "1 - Péssimo"),
        (2, "2 - Ruim"),
        (3, "3 - Regular"),
        (4, "4 - Bom"),
        (5, "5 - Excelente"),
    ]

    proposta = models.ForeignKey(Proposta, on_delete=models.SET_NULL, null=True)
    data_avaliacao = models.DateTimeField(default=timezone.now)
    comentario = models.TextField()
    nota = models.IntegerField(choices=Nota) 