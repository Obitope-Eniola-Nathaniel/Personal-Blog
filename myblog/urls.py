from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('article/<int:id>/', views.article_page, name='article_page'),

    path('register/', views.register, name='register'),
    path('admin-user/', views.admin, name='admin'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
]