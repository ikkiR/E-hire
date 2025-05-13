
#ATENÇÃO ESTE CÓDIGO É APENAS PARA GERAR DADOS FAKES PARA DEMONSTRAÇÃO, ISSO NÃO DEVE SER ENVIADO PARA PRODUÇÃO!!

import os
import sys
from pathlib import Path
from random import choice

import django
from django.conf import settings
from faker import Faker
from django.utils import timezone

# Caminho base do projeto
DJANGO_BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(DJANGO_BASE_DIR))

# Configuração do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False
django.setup()

# Importar o modelo após configurar o Django
from business.models import Empresa

# Instanciar Faker com localização brasileira
fake = Faker('pt_BR')

# Apagar empresas antigas (opcional)
Empresa.objects.all().delete()

# Criar 1000 empresas falsas
for _ in range(100):
    Empresa.objects.create(
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
        create_date=timezone.now(),
    )

print("✅ 1000 empresas criadas com sucesso no banco de dados.")