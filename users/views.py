from .models import Employee
from .models import *
from .serializers import *
from django.contrib.auth.models import User, Permission
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import auth
from .permissions import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    """
    Vista que permite obtener un Token csrf para ser usado en los formularios
    
    Returns:
        HttpResponse csrf_cookie
    """
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})

class LoginView(ObtainAuthToken):
    """
    Vista que permite a un usuario loguearse y retorna un Token de autentificación
    
    Args:
        username : Correo del usuario
        password : Contraseña del usuario
    
    Returns:
        HttpResponse:
        {
            'token': token.key,
            'name': employee.first_name + " "+employee.last_name,
            'role': employee.role,
            'photo': str(employee.photo),
        }
    """
    permissions_classes=[IsUserActivate,]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        employee = user.employee
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'name': employee.first_name + " "+employee.last_name,
            'role': employee.role,
            'photo': str(employee.photo),
        })

class CheckAuthenticatedView(APIView):
    """
    Chequea que el usuario este autentificado y envia los datos del empleado

    Args:
        token : token que asegura que el usuario este autentificado
    Returns:
        HttpResponse:
        {
            'isAuthenticated': 'success',
            'name': employee.first_name + " "+employee.last_name,
            'role': employee.role,
            'photo': str(employee.photo),
        }
    """
    def get(self, request, format=None):
        user = request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                employee = user.employee
                return Response({
                    'isAuthenticated': 'success',
                    'name': employee.first_name + " "+employee.last_name,
                    'role': employee.role,
                    'photo': str(employee.photo),
                    })
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})

class LogoutView(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# ---------------------Vistas Genericas------------------------------


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


# ---------------------Vistas Personalizadas------------------------------

#REGISTRAR USUARIO
@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]

    def post(self, request, format=None):
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        program_code = data['program_code']
        role = data['role']
        phone = data['phone']
        email = data['email']
        password = data['password']
        re_password = data['re_password']
        """Validamos que las contraseñas sean iguales"""
        if password == re_password:
            """Validamos que el usuario no exista"""
            if User.objects.filter(username=email).exists():
                return Response({'error': 'El correo ya existe'})
            else:
                if len(password) < 6:
                    return Response({'error': 'La contraseña debe tener al menos 6 caracteres'})
                else:
                    user = User.objects.create_user(
                        username=email, password=password)
                    user.save()
                    user = User.objects.get(id=user.id)
                    program = Program.objects.get(id=program_code)
                    emp = Employee.objects.create(
                        code="",
                        first_name=first_name,
                        last_name=last_name,
                        role=role,
                        address=address,
                        phone=phone,
                        photo="",
                        estatus="1",
                        user=user,
                        program_code=program
                    )
                    emp.save()
                    return Response({'success': 'Usuario creado con exito'})
        else:
            return Response({'error': 'Las contraseñas no coinciden'})

#ELIMINAR PERFIL USUARIO LOGUEADO
class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        try:
            User.objects.filter(id=user.id).delete()
            return Response({'success': 'Usuario eliminado exitosamente'})
        except:
            return Response({'error': 'Se produjo un error al intentar eliminar al usuario'})

#CONSULTAR PERFIL USUARIO LOGUEADO
class GetUserView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            emp = user.employee
            emp = EmployeeSerializer(emp)
            username = user.username
            user = User.objects.get(id=user.id)
            return Response({"Employee": emp.data, 'username': str(username)})
        except:
            return Response({'error': 'Algo salió mal al recuperar el perfil'})

#MODIFICAR PERFIL USUARIO LOGUEADO
class UpdateUserView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user = User.objects.get(id=user.id)
            data = self.request.data
            address = data['address']
            Employee.objects.filter(user=user).update(address=address)
            emp = user.employee
            emp = EmployeeSerializer(emp)
            return Response({'CustomUser': emp.data, 'username': str(username)})
        except:
            return Response({'error': 'Algo salió mal al actualizar el perfil'})

#LISTAR USUARIOS
class ListUserView(APIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    def get(self, request, format=None):

        try:
            employee = Employee.objects.all()
            employee = EmployeeSerializer(employee, many=True)
            return Response(employee.data)
        except:
            return Response({'error': 'Algo salió mal al listar los Usuarios'})

#ACTIVAR/DESACTIVAR USUARIO
class UserDetailView(APIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]

    def delete(self, request, pk):
        employee = Employee.objects.get(code = pk)
        if employee:
            if employee.status == True:
                Employee.objects.filter(code = pk).update(status='False')
                User.objects.filter(id=employee.user_id).update(is_active='False')
                return Response({'success': 'Usuario desactivado exitosamente'})
            elif employee.status == False:
                Employee.objects.filter(code = pk).update(status='True')
                User.objects.filter(id=employee.user_id).update(is_active='True')
                return Response({'success': 'Usuario activado exitosamente'})
        return Response({'error': 'No existe un Usuario con esos datos'})

#MODIFICAR USUARIO
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]

    def put(self, request, pk):
        employee = Employee.objects.get(code = pk)
        if employee:
            data = self.request.data
            first_name = data['first_name']
            last_name = data['last_name']
            program_code = data['program_code']
            role = data['role']
            address = data['address']
            phone = data['phone']
            photo = data['photo']

            Employee.objects.filter(code = pk).update(first_name=first_name, last_name=last_name, program_code=program_code, role=role, address=address, phone=phone, photo=photo)
            emp = Employee.objects.get(code = pk)
            emp = EmployeeSerializer(emp)
            return Response({ 'Users': emp.data})
        else:
            return Response({ 'error': 'El usuario a modificar no existe' })

#CONSULTAR USUARIO ESPECIFICO
class UserView(APIView):
    permission_classes = [IsAuthenticatedAndAdminUser, ]
    def get(self, request, pk):
        
        try:
            emp = Employee.objects.get(code = pk)
            emp = EmployeeSerializer(emp)
            return Response({ 'Users': emp.data})
        except:
            return Response({ 'error': 'Algo salió mal mostrar el Usuario' })