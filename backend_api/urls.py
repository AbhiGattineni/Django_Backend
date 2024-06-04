from django.urls import path
from . import views
from django.urls import path
from . import views
from .views import (
    TodoListApiView,
    TodoDetailApiView,
    create_status,
    delete_status_by_id,
    get_status,
    # get_status_by_id,
    log_first_time_user,
    update_status_by_id
)

from .views import AddRoleView, GetRoleView, GetAllRolesView, UpdateRoleView, DeleteRoleView

from backend_api.views import acsParttimerStatus_detail, acsParttimerStatus_update, acsParttimerStatus_create, acsParttimerStatus_delete, application_list, application_detail_by_id_and_date
from .views import create_college, get_college, update_college, delete_college, get_all_colleges,user_data_and_roles_view, assign_role, create_part_timer
from .views import ConsultantCreateAPIView, ConsultantListAPIView, ConsultantDeleteAPIView, ConsultantUpdateAPIView, DeleteUserAccessRoleView, PackageListCreateView, PackageDetailView


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
    path('colleges/create/', create_college, name='create_college'),
    path('colleges/all/', get_all_colleges, name='get_all_colleges'),
    path('colleges/<int:pk>/', get_college, name='get_college'),
    path('colleges/<int:pk>/update/', update_college, name='update_college'),
    path('colleges/<int:pk>/delete/', delete_college, name='delete_college'),
    path('user/log-first-time/', log_first_time_user, name='log_first_time_user'),
    path('api/user_and_role_overview/', user_data_and_roles_view, name='user_and_role_overview'),
    path('assignrole/', assign_role, name='assign_role'),
    path('deleteRole/<int:role_id>/', DeleteUserAccessRoleView.as_view(), name='delete_role'),
    path('part-timer/', create_part_timer, name='create_part_timer'),
    path('get-part-timer/<str:user_id>/', views.get_part_timer, name='get_part_timer'),
    path('packages/', PackageListCreateView.as_view(), name='package-list-create'),
    path('packages/<int:pk>/', PackageDetailView.as_view(), name='package-detail'),
    path('acs_parttimer_status/<str:parttimer_id>', acsParttimerStatus_detail),
    path('acs_parttimer_status_create', acsParttimerStatus_create),
    path('acs_parttimer_status_update', acsParttimerStatus_update),
    path('acs_parttimer_status_delete', acsParttimerStatus_delete),
    path('acs_parttimer_status_all', application_list),
    path('acs_parttimer_status/<str:id>/<str:date>', application_detail_by_id_and_date),
    path('create_status_update', create_status, name='create_status_update'),
    path('get_status_update', get_status, name='get_status_update'),
    # path('get_status_by_id/<str:user_id>', get_status_by_id, name='get_status_by_id'),
    path('update_status_by_id', update_status_by_id, name='update_status_by_id'),
    path('delete_status_by_id', delete_status_by_id, name='delete_status_by_id')
]