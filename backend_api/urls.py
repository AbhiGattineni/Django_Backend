from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoDetailApiView
)
from . import views

urlpatterns = [
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('person/create/', views.create_person, name='create_person'),
    path('person/<int:pk>/', views.get_person, name='get_person'),
]