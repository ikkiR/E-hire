from django.contrib import admin
from business import models


from django.contrib.auth.admin import UserAdmin

@admin.register(models.Categoria)
class CategoriaAdmin (admin.ModelAdmin):
    list_display = 'id','name',
    ordering = '-id',
    search_fields = 'id', 'name',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'name',



@admin.register(models.Empresa)
class EmpresaAdmin( admin.ModelAdmin):
    list_display = 'id','tradingName', 'cnpj', 'companyEmail', 'companyPhone', 'city', 'country',
    ordering = '-id',
    list_filter = 'create_date',
    search_fields = 'id', 'trandingName', 'cnjp',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'tradingName',


@admin.register(models.Servico)
class ServicoAdmin (admin.ModelAdmin):
    list_display = 'id','titulo','categoria','empresa'
    ordering = '-id',
    search_fields = 'id', 'titulo', 'categoria', "empresa",
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'titulo',


@admin.register(models.Proposta)
class PropostaAdmin (admin.ModelAdmin):
    list_display = 'id','servico', 'empresa_contratante', 'empresa_prestadora','status'
    ordering = '-id',
    list_filter = 'status',
    search_fields = 'id', 'empresa_prestadora', 'servico', "empresa_contratante",
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id',

@admin.register(models.Avaliacao)
class AvaliacaoAdmin (admin.ModelAdmin):
    list_display = 'id','proposta','nota'
    ordering = '-id',
    list_filter = 'nota',
    search_fields = 'id', 'proposta',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', "proposta",



class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Carteira", {'fields': ('moeda',)}),
    )
    list_display = UserAdmin.list_display + ('moeda',)

admin.site.register(models.Usuario, UsuarioAdmin)
