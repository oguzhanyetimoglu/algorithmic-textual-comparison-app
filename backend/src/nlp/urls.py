from django.urls import path
from . import views

urlpatterns = [
    path('clustering', views.clustering, name='clustering'),
    path('similarity', views.similarity, name='similarity'),
]
