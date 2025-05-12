from django.contrib import admin
from business import models


@admin.register(models.Empresa)
class EmpresaAdmin( admin.ModelAdmin):
    ...
