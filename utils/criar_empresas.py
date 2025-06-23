# ATENÇÃO: ESTE SCRIPT É PARA DEMONSTRAÇÃO — NÃO ENVIAR PARA PRODUÇÃO!

import os
import sys
from pathlib import Path
from random import choice, randint, uniform
from decimal import Decimal

import django
from django.conf import settings
from faker import Faker
from django.utils import timezone
from datetime import date, timedelta

# Caminho base do projeto
DJANGO_BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(DJANGO_BASE_DIR))

# Configuração do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False
django.setup()

# Importar os modelos
from business.models import Empresa, Categoria, Servico, Proposta, Avaliacao

# Instanciar Faker
fake = Faker('pt_BR')

# Limpar dados anteriores (opcional)
Empresa.objects.all().delete()
Categoria.objects.all().delete()
Servico.objects.all().delete()
Proposta.objects.all().delete()
Avaliacao.objects.all().delete()

# Criar categorias
categorias = []
for _ in range(5):
    categoria = Categoria.objects.create(name=fake.word().capitalize())
    categorias.append(categoria)

# Criar empresas
empresas = []
for _ in range(50):
    empresa = Empresa.objects.create(
        companyName=fake.company(),
        tradingName=fake.company_suffix(),
        cnpj=fake.cnpj(),
        stateRegistration=str(fake.random_number(digits=9, fix_len=True)),
        companyEmail=fake.company_email(),
        companyPhone=fake.phone_number(),
        cep=fake.postcode(),
        address=fake.street_name(),
        number=str(fake.building_number()),
        complement=choice(["Bloco A", "Apto 101", "Sala 3", "Fundos", "Casa 2"]),
        neighborhood=fake.bairro(),
        city=fake.city(),
        state=fake.estado_sigla(),
        country=fake.current_country(),
        password=fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        sobre="Somos uma empresa dedicada a fornecer soluções de alta qualidade para nossos clientes.",
        create_date=timezone.now(),
    )
    empresas.append(empresa)

# Criar serviços
servicos = []
for _ in range(30):
    servico = Servico.objects.create(
        titulo=fake.catch_phrase(),
        descricao_rapida=fake.paragraph(),
        descricao_detalhada = fake.paragraph(),
        preco_estimado=Decimal(round(uniform(500, 20000), 2)),
        categoria=choice(categorias),
        empresa=choice(empresas),
        prazo_estimado=date.today() + timedelta(days=randint(5, 30))
    )
    servicos.append(servico)

# Criar propostas
propostas = []
for _ in range(60):
    servico = choice(servicos)

    # Garante que serviço tenha empresa vinculada
    if not servico.empresa:
        continue

    empresa_contratante = choice(empresas)
    empresa_prestadora = choice(empresas)

    # Evita contratar a si mesmo
    while empresa_contratante == empresa_prestadora:
        empresa_prestadora = choice(empresas)

    proposta = Proposta.objects.create(
        servico=servico,
        empresa_contratante=empresa_contratante,
        empresa_prestadora=empresa_prestadora,
        data_proposta=date.today() - timedelta(days=randint(0, 90)),
        status=choice(['PD', 'AC', 'RC', 'FN']),
        valor_negociado=Decimal(round(uniform(300, 25000), 2)),
        prazo_negociado=f"{randint(5, 40)} dias",
        descricao_proposta = "serviço de construção de software"
    )
    propostas.append(proposta)

# Criar avaliações para propostas finalizadas
for proposta in propostas:
    if proposta.status == 'FN':
        Avaliacao.objects.create(
            proposta=proposta,
            data_avaliacao=timezone.now(),
            comentario=fake.sentence(),
            nota=randint(1, 5)
        )

print("✅ Dados fakes gerados com sucesso!")
