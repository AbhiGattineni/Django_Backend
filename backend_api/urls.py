from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoDetailApiView,
)
from . import views

urlpatterns = [
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('person/create/', views.create_person, name='create_person'),
    path('person/<int:pk>/', views.get_person, name='get_person'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/<int:role_id>/', views.get_role, name='get_role'),
    path('roles/update/<int:role_id>/', views.update_role, name='update_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('roles/all/', views.get_all_roles, name='get_all_roles'),
]