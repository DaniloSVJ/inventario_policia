from rest_framework import serializers
from .models import Pessoa,PossePessoaObjeto,Arma,Carro,Computador,CompartilhamentoCarro,RegistroArmas

class PessoaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pessoa 
        fields = [
            'id',
            'nome',
            'cpf', 
            'email',
            'telefone',
            'policial',
            'criacao' ,
            'atualizacao' ,
            'ativo' ,
        ]

class PossePessoaObjetoSerializers(serializers.ModelSerializer):

    class Meta:
        model = PossePessoaObjeto 
        fields = [
            'id',
            'pessoa',
            'carro',
            'arma',
            'computador',
            'criacao' ,
            'atualizacao' ,
            'ativo' ,
        ]


class ArmaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Arma 
        fields = [
            'id',
            'tipoarma',
            'calibre',
            'n_serie',
            'criacao',
            'atualizacao',
            'ativo'
        ]
class RegistroArmasSerializers(serializers.ModelSerializer):

    class Meta:
        model = RegistroArmas
        fields = [
            'id',
            'n_registro',
            'arma',
            'criacao',
            'atualizacao',
            'ativo',
        ]

class ComputadorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Computador 
        fields = [
            'id',
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
        ]     

class CarroSerializers(serializers.ModelSerializer):

    class Meta:
        model = Carro 
        fields = [
            'id',
            'modelo', 
            'placa', 
            'capacidade_pessoas', 
            'viatura', 
            'criacao', 
            'atualizacao', 
            'ativo', 
        ]                


class CompartilhamentoCarroSerializers(serializers.ModelSerializer):

    class Meta:
        model = CompartilhamentoCarro 
        fields = [
            'id',
            'pessoa',
            'carro',
            'criacao',
            'atualizacao',
            'ativo'
        ]