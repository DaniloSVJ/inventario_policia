from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, Permission,Group
from django.contrib.auth.models import User 

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class Carro(models.Model):
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=15)
    capacidade_pessoas = models.DecimalField(max_digits=2,decimal_places=1)
    viatura = models.BooleanField(default=False)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

    def __str__(self):
        return self.modelo

class Arma(models.Model):
    tipoarma = models.CharField(max_length=50)
    calibre = models.CharField(max_length=10)
    n_serie = models.CharField(unique=True,max_length=50)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Arma'
        verbose_name_plural = 'Armas'

    def __str__(self):
        return self.n_serie
    
class Computador(models.Model):
    n_patrimonio = models.CharField(unique=True,max_length=50)
    marca = models.CharField(max_length=20)
    processador = models.CharField(max_length=20)
    tipo_ram = models.CharField(max_length=20)
    qtd_ram = models.DecimalField(max_digits=2,decimal_places=1)
    tip_per_armazenamento = models.CharField(max_length=3)
    qtd_memoria = models.DecimalField(max_digits=2,decimal_places=1)
    so = models.CharField(max_length=20)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Computador'
        verbose_name_plural = 'Computadores'

    def __str__(self):
        return self.n_patrimonio    

class Pessoa(models.Model):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.deletion.CASCADE,
    #     verbose_name=('user'),
    # )
    nome = models.CharField(max_length=250)
    cpf = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    policial = models.BooleanField(default=False)
    #password = models.CharField(max_length=20)
    arma = models.OneToOneField(Arma, on_delete=models.CASCADE,null=True,blank=True)
    computador = models.OneToOneField(Computador, on_delete=models.CASCADE,null=True,blank=True)
    carros = models.ManyToManyField(Carro,through='CompartilhamentoCarro' ,  blank=True)    

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome
    
  

class PossePessoaObjeto(models.Model):
   
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pessoa_posse')  
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    computador = models.ForeignKey(Computador, on_delete=models.CASCADE)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pessoa posse Objeto'
        verbose_name_plural = 'Pessoas posse Objeto'
        unique_together = (('carro', 'pessoa'))
        unique_together = (('arma', 'pessoa'))
        unique_together = (('computador', 'pessoa'))

     
class CompartilhamentoCarro(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='carro_pessoa')

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Compartilhamento de Carro'
        verbose_name_plural = 'Compartilhamento de Carros'
        unique_together = (('carro', 'pessoa'))
   
    def __str__(self):
        return self.carro.placa


class RegistroArmas(models.Model):
    n_registro = models.CharField(unique=True,max_length=50)
    arma = models.ForeignKey(Arma,related_name='avaliacao',on_delete=models.CASCADE)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Resgistro Arma'
        verbose_name_plural = 'Resgistro Armas'

    def __str__(self):
        return self.n_registro

























    