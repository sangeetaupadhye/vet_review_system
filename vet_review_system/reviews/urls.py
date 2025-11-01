from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  
    path('veterinarians/', views.veterinarian_list, name='veterinarian_list'),
    path('add_review/', views.add_review, name='add_review'),
    path('ratings/', views.vet_ratings, name='vet_ratings'),
]
