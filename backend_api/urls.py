from django.urls import path
from . import views
from django.urls import path
from . import views
from .views import (
    TodoListApiView,
    TodoDetailApiView,
    create_status,
    get_status_ids,
    delete_status_by_id,
    get_status,
    # get_status_by_id,
    log_first_time_user,
    update_status_by_id
)

from .views import AddRoleView, GetRoleView, GetAllRolesView, UpdateRoleView, DeleteRoleView

from backend_api.views import acsParttimerStatus_detail, acsParttimerStatus_update, acsParttimerStatus_create, acsParttimerStatus_delete, application_list, application_detail_by_id_and_date
from .views import create_college, get_college, update_college, delete_college, get_all_colleges,user_data_and_roles_view, assign_role, create_part_timer, get_status_by_id, health_check
from .views import ConsultantCreateAPIView, ConsultantListAPIView, ConsultantDeleteAPIView, ConsultantUpdateAPIView, DeleteUserAccessRoleView, PackageListCreateView, PackageDetailView
from .views import (
    EmployerListCreateAPIView, EmployerRetrieveUpdateDeleteAPIView,
    RecruiterListCreateAPIView, RecruiterRetrieveUpdateDeleteAPIView,
    StatusConsultantListCreateAPIView, StatusConsultantRetrieveUpdateDeleteAPIView,HappinessIndexListView
)
from .views import(
submit_happiness_index,get_happiness_index
)
from .views import(
submit_happiness_index,get_happiness_index,get_all_happiness_indexes
)

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
    path('get_status_ids', get_status_ids, name='get_status_ids'),
    path('get_status_by_id/<str:user_id>', get_status_by_id, name='get_status_by_id'),
    path('update_status_by_id', update_status_by_id, name='update_status_by_id'),
    path('delete_status_by_id', delete_status_by_id, name='delete_status_by_id'),
    path('college_details/', views.get_college_details, name='get_college_details'),
    path('college_details/create/', views.create_college_detail, name='create_college_detail'),
    path('college_details/<int:pk>/update/', views.update_college_detail, name='update_college_detail'),
    path('college_details/<int:pk>/delete/', views.delete_college_detail, name='delete_college_detail'),
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/<int:pk>/', views.get_single_product, name='get_single_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/delete/<int:pk>/',views.delete_product,name="delete_product"),
    path('products/update/<int:pk>/',views.update_product,name="update_product"),
    path('employers/', EmployerListCreateAPIView.as_view(), name='employer-list-create'),
    path('employers/<int:pk>/', EmployerRetrieveUpdateDeleteAPIView.as_view(), name='employer-detail'),

    # Recruiter URLs
    path('recruiters/', RecruiterListCreateAPIView.as_view(), name='recruiter-list-create'),
    path('recruiters/<int:pk>/', RecruiterRetrieveUpdateDeleteAPIView.as_view(), name='recruiter-detail'),

    # StatusConsultant URLs
    path('status-consultants/', StatusConsultantListCreateAPIView.as_view(), name='status-consultant-list-create'),
    path('status-consultants/<int:pk>/', StatusConsultantRetrieveUpdateDeleteAPIView.as_view(), name='status-consultant-detail'),
    path('health/', health_check, name='health_check'),

    #Team Members urls
    path('team_members/', views.get_all_team_members, name='get_all_team_members'),
    path('team_members/<int:pk>/', views.get_single_team_member, name='get_single_team_member'),
    path('team_members/add/', views.add_team_member, name='add_team_member'),
    path('team_members/delete/<int:pk>/',views.delete_team_member,name="delete_team_member"),
    path('team_members/update/<int:pk>/',views.update_team_member,name="update_team_member"),

    path('devices/', views.get_all_devices, name='get_all_devices'),
    path('devices/<int:pk>/', views.get_single_device, name='get_single_device'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/delete/<int:pk>/', views.delete_device, name='delete_device'),
    path('devices/update/<int:pk>/', views.update_device, name='update_device'),

    path('happiness-index/add/<str:user_id>/', views.submit_happiness_index, name='submit_happiness_index'),
    path('happiness-index/<str:user_id>/', views.get_happiness_index, name='get_happiness_index'),
    path('happiness/', HappinessIndexListView.as_view(), name='happiness-index-list'),
    path('happiness-index/', views.get_all_happiness_indexes, name='get_all_happiness_indexes'),

]