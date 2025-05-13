from django.db import models
from django.utils import timezone

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
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    def __str__(self) -> str:
        return f'{self.tradingName}'