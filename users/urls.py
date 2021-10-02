from django.urls import path
from rest_framework import views
from .views import *


urlpatterns = [
    path('users/', UserList.as_view(), name = 'user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name = 'user_create'),
    path('employee/', EmployeeList.as_view()),
    path('employee/<int:pk>/', EmployeeDetail.as_view()),
    path('register/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('delete/', DeleteAccountView.as_view()),
    path('csrf_cookie/', GetCSRFToken.as_view()),
    path('users_employee/', GetUserView.as_view()),
    path('update/', UpdateUserView.as_view()),
    path('list/', ListUserView.as_view()),
    path('user/list/', ListUserView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view())
]