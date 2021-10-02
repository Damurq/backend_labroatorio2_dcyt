from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework import generics
from rest_framework.serializers import Serializer

from rest_framework.parsers import FormParser,MultiPartParser

from pensum.models import *
from pensum.serializers import *


#PROGRAM
#LISTADO
class ProgramListAPIView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(is_active = True)

#CREAR
class ProgramCreateAPIView(generics.CreateAPIView):
    serializer_class = ProgramSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#CONSULTA ESPECIFICA
class ProgramDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProgramSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

#ACTUALIZACION
class ProgramUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(code = pk).first()

    def patch(self,request,pk=None):
        if self.get_queryset(pk):
            program_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(program_serializer.data,status = status.HTTP_200_OK)
        return Response({'message': 'No existe un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        if self.get_queryset(pk):
            program_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if program_serializer.is_valid():
                program_serializer.save()
                return Response(program_serializer.data, status = status.HTTP_201_CREATED)
        return Response(program_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#CAMBIO DE ESTADO
class ProgramChangeStateAPIView(generics.DestroyAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def delete(self, request, pk):
        program = self.get_queryset().filter(code = pk).first()
        if program:
            if program.is_active == True:
                program.is_active = False
                program.save()
                return Response({'message': '¡Programa desactivado correctamente!'}, status = status.HTTP_200_OK)
            elif program.is_active == False:
                program.is_active = True
                program.save()
                return Response({'message': '¡Programa activado correctamente!'}, status = status.HTTP_200_OK)
        return Response({'message': 'No existe un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)



#PENSUM
#LISTADO
class PensumListAPIView(generics.ListAPIView):
    serializer_class = PensumSerializer

    def get_queryset(self):
        return Pensum.objects.all()

#CREAR
class PensumCreateAPIView(generics.CreateAPIView):
    serializer_class = PensumSerializer
    parser_classes = [MultiPartParser,FormParser]
    def post(self,request):
        print("here")
        serializer = self.serializer_class(data = request.data)
        print(str(request.data))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        # else:
        #     print("ya tu sabes")
        #     return Response(serializer.data, status = status.HTTP_201_CREATED)
        print(serializer.is_valid())
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#CONSULTA ESPECIFICA
class PensumDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PensumSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()


#ACTUALIZACION
class PensumUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PensumSerializer

    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(code = pk).first()

    def patch(self,request,pk=None):
        if self.get_queryset(pk):
            pensum_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(pensum_serializer.data,status = status.HTTP_200_OK)
        return Response({'message': 'No existe un pensum con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        if self.get_queryset(pk):
            pensum_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if pensum_serializer.is_valid():
                pensum_serializer.save()
                return Response(pensum_serializer.data, status = status.HTTP_201_CREATED)
        return Response(pensum_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#CAMBIO DE ESTADO
class PensumChangeStateAPIView(generics.DestroyAPIView):
    serializer_class = PensumSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def delete(self, request, pk):
        pensum = self.get_queryset().filter(code = pk).first()
        if pensum:
            if pensum.is_active == True:
                pensum.is_active = False
                pensum.save()
                return Response({'message': '¡Pensum desactivado correctamente!'}, status = status.HTTP_200_OK)
            elif pensum.is_active == False:
                pensum.is_active = True
                pensum.save()
                return Response({'message': '¡Pensum activado correctamente!'}, status = status.HTTP_200_OK)
        return Response({'message': 'No existe un pensum con esos datos'}, status = status.HTTP_400_BAD_REQUEST)


        

""""
@api_view(['GET', 'POST'])
def program_api_view(request):

    if request.method == 'GET':
        
        program = Program.objects.all()
        program_serializer = ProgramSerializer(program, many = True)
        return Response(program_serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':

        program_serializer = ProgramSerializer(data = request.data)
        if program_serializer.is_valid():
            program_serializer.save()
            return Response(program_serializer.data, status = status.HTTP_201_CREATED)
        return Response(program_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def program_detail_api_view(request, pk):

    program = Program.objects.filter(code = pk).first()

    if program:

        if request.method == 'GET':
            program_serializer = ProgramSerializer(program)
            return Response(program_serializer.data, status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            program_serializer = ProgramSerializer(program, data = request.data)
            if program_serializer.is_valid():
                program_serializer.save()
                return Response(program_serializer.data, status = status.HTTP_200_OK)
            return Response(program_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            program.delete()
            return Response({'message': '¡Programa eliminado de forma exitosa!'}, status = status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def pensum_api_view(request):

    if request.method == 'GET':
        
        pensum = Pensum.objects.all()
        pensum_serializer = PensumSerializer(pensum, many = True)
        return Response(pensum_serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':

        pensum_serializer = PensumSerializer(data = request.data)
        if pensum_serializer.is_valid():
            pensum_serializer.save()
            return Response(pensum_serializer.data, status = status.HTTP_201_CREATED)
        return Response(pensum_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def pensum_detail_api_view(request, pk):

    pensum = Pensum.objects.filter(code = pk).first()

    if pensum:

        if request.method == 'GET':
            pensum_serializer = PensumSerializer(pensum)
            return Response(pensum_serializer.data, status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            pensum_serializer = PensumSerializer(pensum, data = request.data)
            if pensum_serializer.is_valid():
                pensum_serializer.save()
                return Response(pensum_serializer.data, status = status.HTTP_200_OK)
            return Response(pensum_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            pensum.delete()
            return Response({'message': '¡Pensum eliminado de forma exitosa!'}, status = status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un pensum con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

"""