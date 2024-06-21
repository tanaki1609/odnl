from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view),  # POST->registration
    path('authorization/', views.authorization_api_view),  # POST->authorization
]
