from .models import *
from .serializers import *
from rest_framework import generics
from django.contrib.auth.models import User, Permission
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import auth

#---------------------Vistas Genericas------------------------------
class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from .models import Employee

#---------------------Vistas Personalizadas------------------------------
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        first_name= data['first_name']
        last_name= data['last_name']
        address=data['address']
        program_code = data['program_code']
        role = data['role']
        phone=data['phone']
        email = data['email']
        password = data['password']
        re_password  = data['re_password']
        """Validamos que las contraseñas sean iguales"""
        if password == re_password:
                """Validamos que el usuario no exista"""
                if User.objects.filter(username=email).exists():
                    return Response({ 'error': 'El correo ya existe' })
                else:
                    if len(password) < 6:
                        return Response({ 'error': 'La contraseña debe tener al menos 6 caracteres' })
                    else:
                        user = User.objects.create_user(username=email, password=password)
                        user.save()
                        user = User.objects.get(id=user.id)                        
                        program = Program.objects.get(id=program_code)
                        emp = Employee.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            user=user,
                            program_code = program,
                            role=role,
                            address=address,
                            phone=phone
                        )
                        emp.save()               
                        return Response({ 'success': 'Usuario creado con exito' })
        else:
            return Response({ 'error': 'Las contraseñas no coinciden' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return Response({ 'success': 'Usuario autenticado' })
            else:
                return Response({ 'error': 'Error de autenticación' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Cerrar sesión' })
        except:
            return Response({ 'error': 'Algo salió mal al cerrar la sesión' })

class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        try:
            User.objects.filter(id=user.id).delete()
            return Response({ 'success': 'Usuario eliminado exitosamente' })
        except:
            return Response({ 'error': 'Se produjo un error al intentar eliminar al usuario' })

class GetUserView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            emp = user.employee
            emp = EmployeeSerializer(emp)
            username = user.username
            user=User.objects.get(id=user.id)
            return Response({ "Employee":emp.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Algo salió mal al recuperar el perfil' })

class UpdateUserView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user=User.objects.get(id=user.id)
            data = self.request.data
            address = data['address']
            Employee.objects.filter(user=user).update(address=address)
            emp = user.employee
            emp = EmployeeSerializer(emp)
            return Response({ 'CustomUser': emp.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Algo salió mal al actualizar el perfil' })

class ListUserView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        
        try:
            employee = Employee.objects.all()
            employee = EmployeeSerializer(employee, many=True)
            return Response(employee.data)
        except:
            return Response({ 'error': 'Algo salió mal al listar los Usuarios' })

