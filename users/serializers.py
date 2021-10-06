from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
