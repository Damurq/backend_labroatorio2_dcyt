from django.urls import path
from rest_framework import views
from pensum.views import *


urlpatterns = [
    path('program/list/', ProgramListAPIView.as_view(), name = 'program_list'),
    path('program/create/', ProgramCreateAPIView.as_view(), name = 'program_create'),
    path('program/detail/<int:pk>/', ProgramDetailAPIView.as_view(), name = 'program_detail'),
    path('program/update/<int:pk>/', ProgramUpdateAPIView.as_view(), name = 'program_update'),
    path('program/change/<int:pk>/', ProgramChangeStateAPIView.as_view(), name = 'program_change'),
    path('pensum/list/', PensumListAPIView.as_view(), name = 'pensum_list'),
    path('pensum/create/', PensumCreateAPIView.as_view(), name = 'pensum_create'),
    path('pensum/detail/<int:pk>/', PensumDetailAPIView.as_view(), name = 'pensum_detail'),
    path('pensum/update/<int:pk>/', PensumUpdateAPIView.as_view(), name = 'pensum_update'),
    path('pensum/change/<int:pk>/', PensumChangeStateAPIView.as_view(), name = 'pensum_change'),
    
]