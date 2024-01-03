from django.urls import path
from . import views
from .views import (
    TodoListApiView,
    TodoDetailApiView,
    ConsultantCreateAPIView,
    ConsultantListAPIView,
    ConsultantDeleteAPIView,
    ConsultantUpdateAPIView,
)

from .views import AddRoleView, GetRoleView, GetAllRolesView, UpdateRoleView, DeleteRoleView



urlpatterns = [
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('person/create/', views.create_person, name='create_person'),
    path('person/<int:pk>/', views.get_person, name='get_person'),
    path('roles/add/', AddRoleView.as_view(), name='add_role'),
    path('roles/<int:role_id>/', GetRoleView.as_view(), name='get_role'),
    path('roles/update/<int:role_id>/', UpdateRoleView.as_view(), name='update_role'),
    path('roles/delete/<int:role_id>/', DeleteRoleView.as_view(), name='delete_role'),
    path('roles/all/', GetAllRolesView.as_view(), name='get_all_roles'),
    path('api/consultant/', ConsultantCreateAPIView.as_view(), name='create-consultant'),
    path('api/consultants/', ConsultantListAPIView.as_view(), name='consultant-list'),
    path('consultants/delete/<int:pk>/', ConsultantDeleteAPIView.as_view(), name='consultant-delete'),
    path('api/consultants/<int:pk>/', ConsultantUpdateAPIView.as_view(), name='consultant-update'),
]