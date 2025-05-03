from django.urls import path
from .views import predict_house_price, retrain_model_view

urlpatterns = [
    path('predict-house-price/', predict_house_price),
    path('retrain/', retrain_model_view),
]
