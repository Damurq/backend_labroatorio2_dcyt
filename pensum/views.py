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
        print(data)
        program_code= data['program_code']
        print(data['file_pdf'])
        print(type(data['file_pdf']))
        file_pdf= data['file_pdf']
        description=data['description']
        if Program.objects.filter(code=program_code).exists():
            program=Program.objects.get(code=program_code)
            pensum = Pensum.objects.create(
                  description=description,
                  program_code=program,
                  file_pdf=file_pdf,
                  expiration_date="2020-05-12",
                  date_issue="2030-16-04",
                  is_active="True"
                        )
            pensum.save()
            return Response({ 'success': 'Usuario creado con exito' })
        else:
            return Response({ 'error': 'El correo ya existe' })
            


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
            file_pdf= data['file_pdf']
            description=data['description']

            Pensum.objects.filter(code = pk).update(description=description, file_pdf=file_pdf)
            return Response({ 'success': 'Pensum modificado con exito' })
        else:
            return Response({ 'error': 'El pensum a modificar no existe' })


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

