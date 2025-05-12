from django.urls import path
from business import views



app_name = 'business'

urlpatterns = [
    path('', views.index, name='index'),
]
