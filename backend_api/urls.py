from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoDetailApiView,
)
from . import views
from .views import create_college, get_college, update_college, delete_college
from .views import ConsultantCreateAPIView, ConsultantListAPIView, ConsultantDeleteAPIView, ConsultantUpdateAPIView


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
    path('colleges/', create_college, name='create_college'),
    path('colleges/<int:pk>/', get_college, name='get_college'),
    path('colleges/<int:pk>/update/', update_college, name='update_college'),
    path('colleges/<int:pk>/delete/', delete_college, name='delete_college'),
    path('api/consultant/', ConsultantCreateAPIView.as_view(), name='create-consultant'),
    path('api/consultants/', ConsultantListAPIView.as_view(), name='consultant-list'),
    path('consultants/delete/<int:pk>/', ConsultantDeleteAPIView.as_view(), name='consultant-delete'),
    path('api/consultants/<int:pk>/', ConsultantUpdateAPIView.as_view(), name='consultant-update'),
]