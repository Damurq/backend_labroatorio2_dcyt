from users.models import Employee
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

from users.permissions import *

class ProgramList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def delete(self, request, pk):
        program = self.get_queryset().filter(code = pk).first()
        if program:
            if program.is_active == True:
                pensum = Pensum.objects.filter(program_code = pk, is_active = True).first()
                pensum.is_active = False
                pensum.save()

                program.is_active = False
                program.save()
                return Response({'message': '¡Programa y Pensum asociado desactivados correctamente!'}, status = status.HTTP_200_OK)
            elif program.is_active == False:
                pensum = Pensum.objects.filter(program_code = pk, is_active = False).last()
                pensum.is_active = True
                pensum.save()

                program.is_active = True
                program.save()
                return Response({'message': '¡Programa y ultimo pensum asociado activado correctamente!'}, status = status.HTTP_200_OK)
        return Response({'message': 'No existe un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)


class PensumList(generics.ListCreateAPIView):
    queryset = Pensum.objects.all()
    serializer_class = PensumSerializer

    def get(self, request, format=None):
        user = self.request.user
        emp=Employee.objects.get(user=user.id)
        if emp.role=="A":
            pensum= Pensum.objects.all()
            pensum= PensumSerializer(pensum,many=True)
            return Response(pensum.data)
        elif emp.role=="G": 
            try:
                emp=Employee.objects.get(user=user.id)
                pensum=Pensum.objects.filter(program_code=emp.program_code)
                pensum = PensumSerializer(pensum, many=True)
                return Response(pensum.data)
            except:
                return Response({ 'error': 'Algo salió mal al listar los pensum' })

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            codeP = request.data['program_code']
            active_code_program = Program.objects.filter(is_active = False, code = codeP).first()
            if active_code_program:
                return Response({'message': 'el programa asociado al pensum se encuentra inactivo'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                pensum_anterior = Pensum.objects.filter(is_active = True, program_code = codeP).first()
                if pensum_anterior:
                    pensum_anterior.is_active = False
                    pensum_anterior.save()
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            


class PensumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pensum.objects.all()
    serializer_class = PensumSerializer

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


class NumberPensumProgram(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    
    def get(self, request, pk):
        program = Program.objects.filter(code = pk).first()

        if program:
            pensum = Pensum.objects.filter(program_code = pk).count()
            number_pensum ={
                'name_Pro': program.name,
                'count': pensum
            }
            count_serializer = CountSerializer(data = number_pensum)
            if count_serializer.is_valid():
                return Response(count_serializer.data, status = status.HTTP_200_OK)
        return Response({'message': 'No se ha encontrado un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)


class ProgramPensumListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    serializer_class = ProgramPensumSerializer

    def get_queryset(self):
        return Pensum.objects.select_related("program_code")

