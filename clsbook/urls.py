from django.urls import path
from . import views

app_name = 'clsbook'

urlpatterns = [
    path('', views.clsbook, name='clsbook'),
    path('create/', views.create_classbook, name='create'),
    path('delete/<int:pk>/', views.delete_classbook, name='delete'),
    path('reset/<int:pk>/', views.reset_password, name='reset'),
]
