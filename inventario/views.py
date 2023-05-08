from rest_framework import  generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import mixins
from rest_framework.permissions import BasePermission ,IsAuthenticated
from django.forms import ValidationError
from django.contrib.auth.models import User 
from . import models
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .models import (Pessoa,PossePessoaObjeto,Arma,Carro,
CompartilhamentoCarro,
Computador,RegistroArmas)

from .serializer import ArmaSerializers,PessoaSerializers,PossePessoaObjetoSerializers,CarroSerializers,ComputadorSerializers,CompartilhamentoCarroSerializers,RegistroArmasSerializers

def f_create_user(email,nome,senha):
        user = User.objects.create_user(username=nome,
                                    email=email,
                                    password=senha)
        user.is_active = False
        user.save()  


class IsPolicialOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to non-policial users.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated #and request.user.is_policial()
    
####################### METODOS PESSOA #####################################
class PessoaAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = Pessoa.objects.all()
     serializer_class = PessoaSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]
     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            return self.create(request, *args, **kwargs)
        
         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)


class PessoaAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = Pessoa.objects.all()
     serializer_class = PessoaSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        



####################### METODOS PESSOA OBJETO #####################################
class PossePessoaObjetoAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = PossePessoaObjeto.objects.all()
     serializer_class = PossePessoaObjetoSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]
     def get(self, request, *args, **kwargs):
         try:
            return self.list(request, *args, **kwargs)

         except KeyError:
            dat = {
               "details": "Algo deu errado, aguarde alguns segundos e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
     def post(self, request, *args, **kwargs):
        arma = request.data['arma']
        arma_resgister = RegistroArmas.objects.filter(arma=arma)
        #Regra de Negócio se a arma está registrada no sistema
        if len(arma_resgister)==0:
            dat = {
               "details": "Essa arma não está registrada no sistema."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
        #Regra de Negócio: Objetos dos demais tipos so podem ser possuídos por uma Pessoa por vez.
        arma_posse = PossePessoaObjeto.objects.filter(arma=arma)
        if len(arma_posse)>0:    
            dat = {
               "details": "Essa arma já está na posse de uma pessoa."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
       
        computador = request.data['computador']
        computador_posse = PossePessoaObjeto.objects.filter(computador=computador) 
        if len(computador_posse)>0:    
            dat = {
               "details": "Esse computador já está na posse de uma pessoa."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
        
        #Regra de Negócio: Apenas Policiais Civis podem possuir objetos do tipo viatura policial.
        carro_id = request.data['carro']
        carro = Carro.objects.get(id=carro_id)
        pessoa_id = request.data['pessoa']
        pessoa = Pessoa.objects.get(id=pessoa_id)
       
        if not pessoa.policial: 
            if carro.viatura==True:
               dat = {
                  "details": "A pessoa não é policial, por isso não pode possuir a viatura"
               }
               return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        carro_posse = PossePessoaObjeto.objects.filter(carro=carro_id) 
        if len(carro_posse)==2:    
               dat = {
                  "details": "Esse carro já está sendo usado por duas pessoas."
               }
               return Response(dat, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

class PossePessoaObjetoAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = PossePessoaObjeto.objects.all()
     serializer_class = PossePessoaObjetoSerializers

     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]
     
     def get(self, request, *args, **kwargs):
         try:
            return self.retrieve(request, *args, **kwargs)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verique se você colocou o ID correto e tente novamente."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
  

     def put(self, request, *args, **kwargs):
        arma = request.data['arma']
        arma_resgister = RegistroArmas.objects.filter(arma=arma)
        #Regra de Negócio se a arma está registrada no sistema
        if len(arma_resgister)==0:
            dat = {
               "details": "Essa arma não está registrada no sistema."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
        #Regra de Negócio: Objetos dos demais tipos so podem ser possuídos por uma Pessoa por vez.
        arma_posse = PossePessoaObjeto.objects.filter(arma=arma)
        if len(arma_posse)>0:    
            dat = {
               "details": "Essa arma já está na posse de uma pessoa."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
       
        computador = request.data['computador']
        computador_posse = PossePessoaObjeto.objects.filter(computador=computador) 
        if len(computador_posse)>0:    
            dat = {
               "details": "Esse computador já está na posse de uma pessoa."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
        
        #Regra de Negócio: Apenas Policiais Civis podem possuir objetos do tipo viatura policial.
        carro_id = request.data['carro']
        carro = Carro.objects.get(id=carro_id)
        pessoa_id = request.data['pessoa']
        pessoa = Pessoa.objects.get(id=pessoa_id)
       
        if not pessoa.policial: 
            if carro.viatura==True:
               dat = {
                  "details": "A pessoa não é policial, por isso não pode possuir a viatura"
               }
               return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        carro_posse = PossePessoaObjeto.objects.filter(carro=carro_id) 
        if len(carro_posse)==2:    
               dat = {
                  "details": "Esse carro já está sendo usado por duas pessoas."
               }
               return Response(dat, status=status.HTTP_400_BAD_REQUEST)
         

        try:
            self.update(request, *args, **kwargs)
            dat = {
               "details": "Atualizado com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

        except KeyError:
            dat = {
               "details": "Algo deu errado, verifique as informações e tente novamente."
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)
        
        
        
     def delete(self, request, *args, **kwargs):
        
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        
   


####################### METODOS ARMA #####################################
class ArmaAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = Arma.objects.all()
     serializer_class = ArmaSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            detail = self.create(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_201_CREATED)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)


class ArmaAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = Arma.objects.all()
     serializer_class = ArmaSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]


     
     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)


     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        

####################### METODOS CARRO #####################################
class CarroAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = Carro.objects.all()
     serializer_class = CarroSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]
     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            detail = self.create(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_201_CREATED)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

 
   

class CarroAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = Carro.objects.all()
     serializer_class = CarroSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]


     
     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        

####################### METODOS COMPUTADOR #####################################
class ComputadorAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = Computador.objects.all()
     serializer_class = ComputadorSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            detail = self.create(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_201_CREATED)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

 

class ComputadorAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = Computador.objects.all()
     serializer_class = ComputadorSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]


     
     
     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)



     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        

####################### METODOS COMPARTILHAMENTO CARRO #####################################
class CompartilhamentoCarroAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = CompartilhamentoCarro.objects.all()
     serializer_class = CompartilhamentoCarroSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            detail = self.create(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_201_CREATED)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

   

class CompartilhamentoCarroAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = CompartilhamentoCarro.objects.all()
     serializer_class = CompartilhamentoCarroSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]


     
     
     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)



     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        


####################### METODOS REGISTRO ARMA #####################################
class RegistroArmasAPIViews(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
     queryset = RegistroArmas.objects.all()
     serializer_class = RegistroArmasSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

     def get(self, request, *args, **kwargs):
         try:
            detail = self.list(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, tente novamente após alguns segundos"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def post(self, request, *args, **kwargs):
         try:
            detail = self.create(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_201_CREATED)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao cadastrar, verifique se as informações estão corretas e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)


class RegistroArmaAPIViewsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
     queryset = RegistroArmas.objects.all()
     serializer_class = RegistroArmasSerializers
     permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]


     
     def get(self, request, *args, **kwargs):
         try:
            detail = self.retrieve(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, *args, **kwargs):
         try:
            detail = self.update(request, *args, **kwargs)
            return Response(detail.data, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "details": "Algo deu errado ao atualizar, verifique se o ID está correto e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST)



     def delete(self, request, *args, **kwargs):
         try:
            self.destroy(request, *args, **kwargs)
            dat = {
                'details' : "Excluido com sucesso"
            }
            return Response(dat, status=status.HTTP_200_OK)

         except KeyError:
            dat = {
               "detailss": "Algo deu errado ao excluir, verifique as informações e tente novamente"
            }
            return Response(dat, status=status.HTTP_400_BAD_REQUEST) 
        


################### PESQUISA OBJETO ##########################
class PesqueisaPosseObjetoView(generics.ListAPIView):
    serializer_class = PossePessoaObjetoSerializers
    permission_classes = [IsAuthenticated, IsPolicialOrReadOnly]

    def get_queryset(self):
        n_serie_arma = self.request.query_params.get('n_serie_arma')
        n_patri_computador = self.request.query_params.get('n_patrimonio_computador')
        placa_carro = self.request.query_params.get('placa_carro')
        queryset = PossePessoaObjeto.objects.all()

        if n_serie_arma:
            queryset = queryset.filter(arma__n_serie=n_serie_arma)
            
        if n_patri_computador:
            queryset = queryset.filter(computador__n_patrimonio=n_patri_computador)

        if placa_carro:
            queryset = queryset.filter(carro__placa=placa_carro)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result_list = []
        
        for posse in queryset:
            result_dict = {
                "id": posse.id,
                "pessoa": {
                    "id": posse.pessoa.id,
                    "nome": posse.pessoa.nome,
                    "cpf": posse.pessoa.cpf,
                    "email": posse.pessoa.email,
                    "telefone": posse.pessoa.telefone,
                    "policial": posse.pessoa.policial,
                    "criacao": posse.pessoa.criacao,
                    "atualizacao": posse.pessoa.atualizacao,
                    "ativo": posse.pessoa.ativo
                },
                "carro":{
                    "id": posse.carro.id,
                    "modelo": posse.carro.modelo,
                    "placa": posse.carro.placa,
                    "capacidade_pessoas": posse.carro.capacidade_pessoas,
                    "viatura": posse.carro.viatura,
                    "criacao": posse.pessoa.criacao,
                    "atualizacao": posse.pessoa.atualizacao,
                    "ativo": posse.pessoa.ativo
                },
                "arma": {
                    "id": posse.arma.id,
                    "nome": posse.arma.tipoarma,
                    "cpf": posse.arma.calibre,
                    "email": posse.arma.n_serie,
                    "atualizacao": posse.pessoa.atualizacao,
                    "ativo": posse.pessoa.ativo
                },
                "computador":{
                    "id": posse.computador.id,
                    "n_patrimonio": posse.computador.n_patrimonio,
                    "marca": posse.computador.marca,
                    "processador": posse.computador.processador,
                    "tipo_ram": posse.computador.tipo_ram,
                    "qtd_ram": posse.computador.qtd_ram,
                    "tip_per_armazenamento": posse.computador.tip_per_armazenamento,
                    "qtd_memoria": posse.computador.qtd_memoria,
                    "so": posse.computador.so,
                    "tipo_ram": posse.computador.tipo_ram,
                    "criacao": posse.computador.criacao,
                    "atualizacao": posse.computador.atualizacao,
                    "ativo": posse.computador.ativo,
                },
                "criacao": posse.criacao,
                "atualizacao": posse.atualizacao,
                "ativo": posse.ativo
            }
            result_list.append(result_dict)
        
        return Response(result_list)