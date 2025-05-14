from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadStatementView.as_view(), name='upload-statement'),
]
