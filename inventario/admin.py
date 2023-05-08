from django.contrib import admin

# Register your models here.
from .models import (
    Arma,
    Carro,
    CompartilhamentoCarro,
    Computador,
    Pessoa,
    PossePessoaObjeto,
    RegistroArmas,
    
)


@admin.register(Pessoa)  
class PessoaAdmin(admin.ModelAdmin):
    list_display=(
        'nome',
        'cpf', 
        'email',
        'telefone',
        'policial',
        
        'criacao' ,
        'atualizacao' ,
        'ativo' ,
    )

@admin.register(PossePessoaObjeto)  
class PossePessoaObjetoAdmin(admin.ModelAdmin):
    list_display=(
        'pessoa',
        'carro',
        'arma',
        'computador',
        'criacao' ,
        'atualizacao' ,
        'ativo' ,
    )

@admin.register(Arma)
class ArmaAdmin(admin.ModelAdmin):
    list_display = (
        'tipoarma',
        'calibre',
        'n_serie',
        'criacao',
        'atualizacao',
        'ativo'
    )



@admin.register(RegistroArmas)
class RegistroArmas(admin.ModelAdmin):
    list_display = (
        'n_registro',
        'arma',
        'criacao',
        'atualizacao',
        'ativo',
    )

@admin.register(Carro)    
class CarroAdmin(admin.ModelAdmin):
    list_display = (
        'modelo', 
        'placa', 
        'capacidade_pessoas', 
        'viatura', 
        'criacao', 
        'atualizacao', 
        'ativo', 
    )

@admin.register(CompartilhamentoCarro)
class CompartilhamentoCarroAdmin(admin.ModelAdmin):
    list_display = (
        'carro',
        'pessoa',
     
        'criacao',
        'atualizacao',
        'ativo'
    )

@admin.register(Computador)
class Computador(admin.ModelAdmin):
    list_display = (
        'n_patrimonio',
        'marca',
        'processador',
        'tipo_ram',
        'qtd_ram',
        'tip_per_armazenamento',
        'qtd_memoria',
        'so',
        'criacao',
        'atualizacao',
        'ativo',
    )
