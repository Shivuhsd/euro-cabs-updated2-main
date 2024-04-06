from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('driverRegister/', views.DriverRegister, name='driverRegister'),
    path('otpVerification/', views.OtpVerification, name='otpVerification'),
    path('adminlogin/<str:pk>/', views.adminLogin, name='adminlogin'),
]
