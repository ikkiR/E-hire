from django.contrib import admin
from business import models


@admin.register(models.Empresa)
class EmpresaAdmin( admin.ModelAdmin):
    list_display = 'id','tradingName', 'cnpj', 'companyEmail', 'companyPhone', 'city', 'country',
    ordering = '-id',
    list_filter = 'create_date',
    search_fields = 'id', 'trandingName', 'cnjp',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'tradingName',