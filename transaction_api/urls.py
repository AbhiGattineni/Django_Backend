from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transaction/<str:transaction_id>/', views.get_transaction, name='get_transaction'),
    path('transaction/<str:transaction_id>/update/', views.update_transaction, name='update_transaction'),
    path('transaction/<str:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    # path('transactions/filter/', views.get_transactions_by_fields, name='get_transactions_by_fields'),
    # path('transactions/date-range/', views.transaction_date_range_view, name='transaction-date-range'),
    path('transactions/filter/', views.get_filter_transactions, name='get-filter-transactions'),
]
