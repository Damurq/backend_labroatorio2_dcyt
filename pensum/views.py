from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import permissions

from users.models import Employee
from pensum.models import *
from users.permissions import *
from pensum.serializers import *

#----------------------VISTAS ASOCIADAS A PROGRAMA---------------------
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
            pensum_exists = Pensum.objects.filter(program_code = pk).exists()
            if pensum_exists == False:
                if program.is_active == True:
                    program.is_active = False
                    program.save()
                    return Response({'message': '¡Programa desactivado correctamente!'}, status = status.HTTP_200_OK)
                
                elif program.is_active == False:
                    program.is_active = True
                    program.save()
                    return Response({'message': '¡Programa activado correctamente!'}, status = status.HTTP_200_OK)

            elif pensum_exists == True:
                if program.is_active == True:
                    pensum = Pensum.objects.filter(program_code = pk).last()
                    if pensum.is_active == False:
                        program.is_active = False
                        program.save()
                        return Response({'message': '¡Programa desactivado correctamente!'}, status = status.HTTP_200_OK)
                    elif pensum.is_active == True:
                        pensum.is_active = False
                        pensum.save()
                        program.is_active = False
                        program.save()
                        return Response({'message': '¡Programa y ultimo Pensum asociado desactivados correctamente!'}, status = status.HTTP_200_OK)
                elif program.is_active == False:
                    pensum = Pensum.objects.filter(program_code = pk).last()
                    if pensum.is_active == True:
                        program.is_active = True
                        program.save()
                        return Response({'message': '¡Programa activado correctamente!'}, status = status.HTTP_200_OK)
                        
                    elif pensum.is_active == False:
                        pensum.is_active = True
                        pensum.save()
                        program.is_active = True
                        program.save()
                        return Response({'message': '¡Programa y ultimo pensum asociado activados correctamente!'}, status = status.HTTP_200_OK)
                        
        return Response({'message': 'No existe un programa con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

#-----------------VISTAS ASOCIADAS A PENSUM------------------
class PensumList(generics.ListCreateAPIView):
    queryset = Pensum.objects.all()
    serializer_class = PensumSerializer

    def get(self, request, format=None):
        emp = request.user.employee
        if emp.role=="A":
            pensum= Pensum.objects.all()
            pensum= PensumSerializer(pensum,many=True)
            return Response(pensum.data)
        elif emp.role=="G": 
            try:
                
                pensum=Pensum.objects.filter(program_code=emp.program_code)
                pensum = PensumSerializer(pensum, many=True)
                return Response(pensum.data)
            except:
                return Response({ 'error': 'Algo salió mal al listar los pensum' })

    def post(self, request, format=None):
        data = self.request.data
        program_code= data['program_code']
        commission_code = data['commission_code']
        description=data['description']
        if Program.objects.filter(code=program_code).exists():
            program=Program.objects.get(code=program_code)
            commision = Commission.objects.get(code = commission_code)
            pensum = Pensum.objects.create(
                  description=description,
                  program_code=program,
                  commission_code=commision,
                  expiration_date="2020-05-12",
                  date_issue="2030-16-04",
                  is_active="True"
                        )
            pensum.save()
            return Response({ 'success': 'Pensum creado con exito' })
        else:
            return Response({ 'error': 'El Pensum ya existe' })
            


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
    
    def put(self, request, pk):
        pensum = Pensum.objects.get(code = pk)
        if pensum:
            data = self.request.data
            description=data['description'] 
            commission_code=data['commission_code'] 
            program_code=data['program_code']
            Pensum.objects.filter(code = pk).update(description=description,commission_code=commission_code,program_code=program_code)
            return Response({ 'success': 'Pensum modificado con exito' })
        else:
            return Response({ 'error': 'El pensum a modificar no existe' })

#-------------------VISTAS ASOCIADAS A COMISION--------------------------------
class CommisionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer

class CommissionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    def delete(self, request, pk):
        commission = self.get_queryset().filter(code = pk).first()
        if commission:
            if commission.is_active == True:
                commission.is_active = False
                commission.save()
                return Response({'message': '¡Comision desactivada correctamente!'}, status = status.HTTP_200_OK)
            elif commission.is_active == False:
                commission.is_active = True
                commission.save()
                return Response({'message': '¡Comision activada correctamente!'}, status = status.HTTP_200_OK)
        return Response({'message': 'No existe una comision con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

#-----------------------VISTAS ASOCIADAS A REPORTES---------------------------------
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


class NumberPensumCommission(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    
    def get(self, request, pk):
        commission = Commission.objects.filter(code = pk).first()

        if commission:
            pensum = Pensum.objects.filter(commission_code = pk).count()
            number_pensum ={
                'name_commi': commission.name,
                'count': pensum
            }
            count_serializer = CountPensumCommisionSerializer(data = number_pensum)
            if count_serializer.is_valid():
                return Response(count_serializer.data, status = status.HTTP_200_OK)
        return Response({'message': 'No se ha encontrado una comision con esos datos'}, status = status.HTTP_400_BAD_REQUEST)

class CommissionPensumListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    serializer_class = CommissionPensumSerializer

    def get_queryset(self):
        return Pensum.objects.select_related("commission_code")