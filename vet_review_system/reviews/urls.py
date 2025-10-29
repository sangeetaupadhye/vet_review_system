from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('vets/', views.vet_ratings, name='vet_ratings'),
    path('add-review/', views.add_review, name='add_review'),
]
