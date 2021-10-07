from django.urls import path
from rest_framework import views
from pensum.views import *

urlpatterns = [
    path('program/list/', ProgramList.as_view(), name = 'program_list'),
    path('program/detail/<int:pk>/', ProgramDetail.as_view(), name = 'program_detail'),
    path('pensum/list/', PensumList.as_view(), name = 'pensum_list'),
    path('pensum/detail/<int:pk>/', PensumDetail.as_view(), name = 'pensum_detail'),
    path('program/numberpensum/<int:pk>/', NumberPensumProgram.as_view(), name = 'program_number_pensum'),
    path('program/pensum/list/', ProgramPensumListAPIView.as_view(), name = 'program_pensum'),
    path('commission/list/', CommisionList.as_view(), name = 'commission_list'),#de aqui empiezan las agregadas
    path('commission/detail/<int:pk>/', CommissionDetail.as_view(), name = 'commission_detail'),
    path('commission/numberpensum/<int:pk>/', NumberPensumCommission.as_view(), name = 'commission_number_pensum'),
    path('commission/pensum/list/', CommissionPensumListAPIView.as_view(), name = 'commission_pensum'),
    
]