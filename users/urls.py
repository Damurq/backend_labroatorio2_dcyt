from django.urls import path
from rest_framework import views
from .views import *


urlpatterns = [
    path('users/', UserList.as_view(), name = 'user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name = 'user_create'),
    path('employee/', EmployeeList.as_view()),
    path('employee/<int:pk>/', EmployeeDetail.as_view()),
]