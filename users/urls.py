from django.urls import path
from .views import *


urlpatterns = [
    path('csrf_cookie/', GetCSRFToken.as_view()),
    path('login/', LoginView.as_view()),
    path('checkAuthenticated',CheckAuthenticatedView.as_view(), name = 'CheckAuthenticatedView'),
    path('logout/', LogoutView.as_view()),
    path('user/users/', UserList.as_view(), name = 'user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name = 'user_create'),
    path('user/employee/', EmployeeList.as_view()),
    path('user/employee/<int:pk>/', EmployeeDetail.as_view()),
    path('user/register/', SignupView.as_view()),
    path('user/delete/', DeleteAccountView.as_view()),
    path('user/users_employee/', GetUserView.as_view()),
    path('user/list/', ListUserView.as_view()),
    path('user/detaill/<int:pk>/', UpdateUserView.as_view()),
    path('user/detail/<int:pk>/', UserDetailView.as_view()),
    path('user/update_user/<int:pk>/', UserUpdateView.as_view()),
    path('user/user/<int:pk>/', UserView.as_view()),
]