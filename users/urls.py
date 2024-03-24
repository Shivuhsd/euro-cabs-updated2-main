from django.urls import path
from . import views

urlpatterns = [
#     path('/', views.adminDashborad, name='adminDashboard'),
    #Complaint Endpoint
    path('', views.home, name='home'),
    path('privacyAndPolicy/', views.privacyAndPolicy, name='privacyPolicy'),
    path('rides/', views.rides, name='rides'),
    path('websiteTerms/', views.websiteTerms, name='websiteTerms'),
    path('corporate/', views.corporate, name='corporate'),
    path('businessT&C/', views.businessTerms, name='businessTerms'),
    # path('driverRegister/', views.driverRegister, name='driverRegister'),
    path('complaintForm/', views.complaintForm, name='complaintForm'),
    path('businessForm/', views.businessForm, name='businessForm'),
    path('airportDest/', views.airportDest, name='airportDest'),
    path('airports/', views.airports, name='airports'),
    path('schools/', views.schools, name='schools'),
    # path('airportRates/', views.GetAirportRates, name='getAirportRates'),

    #Driver Registration Field

    path('driverForm/', views.DriverForm, name='driverForm'),
    path('driverDash/', views.DriverDash, name='driverDash'),


    ## Users Reply for A complaint Feedback
    path('comreply/<str:pk>/<str:rep>/', views.CusReply, name='cusreply'),
]