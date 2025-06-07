from django.urls import path
from . import views
from .views import add_warehouse

urlpatterns = [
    path('', views.index, name='index'),
    path('add-warehouse/', add_warehouse, name='add_warehouse'),
    path('add-truck/', views.add_truck, name='add_truck'),
]