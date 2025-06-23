from django.db import models
from django.utils import timezone
from datetime import date

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager

# Manager de usuário customizado
class EmpresaManager(BaseUserManager):
    def create_user(self, companyEmail, password=None, **extra_fields):
        if not companyEmail:
            raise ValueError("E-mail obrigatório.")
        email = self.normalize_email(companyEmail)
        user = self.model(companyEmail=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, companyEmail, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(companyEmail, password, **extra_fields)

# Categoria de serviços
class Categoria(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Empresa como usuário
class Empresa(AbstractBaseUser, PermissionsMixin):

    estados = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]

    companyName = models.CharField(max_length=250)
    tradingName = models.CharField(max_length=250, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    stateRegistration = models.CharField(max_length=30, blank=True, null=True)
    companyEmail = models.EmailField(unique=True)
    companyPhone = models.CharField(max_length=20)
    cep = models.CharField(max_length=9)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=estados)
    country = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    sobre = models.TextField(max_length=500, null=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'companyEmail'
    REQUIRED_FIELDS = ['companyName', 'cnpj']

    objects = EmpresaManager()

    def __str__(self):
        return self.tradingName or self.companyName

    def save(self, *args, **kwargs):
        if not self.tradingName:
            self.tradingName = self.companyName
        super().save(*args, **kwargs)

# Serviço oferecido por empresa
class Servico(models.Model):
    disponibilidade_escolhas = [
        ('DISP', 'Disponível'),
        ('IND', 'Indisponível'),
    ]

    titulo = models.CharField(max_length=50)
    descricao_rapida = models.CharField(max_length=100, null=True)
    descricao_detalhada = models.TextField(null=True)
    preco_estimado = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Se a empresa for excluída, apaga o serviço
    prazo_estimado = models.DateField(null=True)
    disponibilidade = models.CharField(max_length=4, choices=disponibilidade_escolhas, default='DISP')

    def __str__(self):
        return self.titulo

# Propostas feitas entre empresas
class Proposta(models.Model):
    status_choices = [
        ('PD', 'Pendente'),
        ('AC', 'Aceita'),
        ('RC', 'Recusada'),
        ('FN', 'Finalizada'),
    ]

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='propostas')  # Se serviço for excluído, apaga proposta
    empresa_contratante = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='propostas_contratadas')  # Se contratante sumir, apaga proposta
    empresa_prestadora = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, related_name='propostas_prestadas')  # Pode ficar nulo
    data_proposta = models.DateField(default=date.today)
    status = models.CharField(max_length=2, choices=status_choices)
    valor_negociado = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    prazo_negociado = models.CharField(max_length=50, blank=True, null=True)
    descricao_proposta = models.TextField(blank=True, null=True)

    def __str__(self):
        prestadora = self.empresa_prestadora.tradingName if self.empresa_prestadora else "Aguardando"
        return f"{self.servico.titulo} - {self.empresa_contratante.tradingName} x {prestadora}"

# Avaliação feita sobre proposta
class Avaliacao(models.Model):
    Nota = [
        (1, "1 - Péssimo"),
        (2, "2 - Ruim"),
        (3, "3 - Regular"),
        (4, "4 - Bom"),
        (5, "5 - Excelente"),
    ]

    proposta = models.ForeignKey(Proposta, on_delete=models.CASCADE, related_name="avaliacoes")  # Se proposta for excluída, exclui avaliação
    data_avaliacao = models.DateTimeField(default=timezone.now)
    comentario = models.TextField()

    nota = models.IntegerField(choices=Nota) 

      def __str__(self):
        return f"Avaliação {self.nota} para {self.proposta}"

class Usuario(AbstractUser):
    moeda = models.IntegerField(default=0)
  
