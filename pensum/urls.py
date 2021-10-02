from django.urls import path
from rest_framework import views
from pensum.views import *

urlpatterns = [
    path('program/list/', ProgramList.as_view(), name = 'program_list'),
    path('program/detail/<int:pk>/', ProgramDetail.as_view(), name = 'program_detail'),
    path('pensum/list/', PensumList.as_view(), name = 'pensum_list'),
    path('pensum/detail/<int:pk>/', PensumDetail.as_view(), name = 'pensum_detail'),
    path('program/numberpensum/<int:pk>/', NumberPensumProgram.as_view(), name = 'program_number_pensum'),
    path('program/pensum/', ProgramPensumListAPIView.as_view(), name = 'program_pensum'),
    
]