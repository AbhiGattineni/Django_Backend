from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
import json
from django.utils.dateparse import parse_datetime

def validate_subsidiary(value):
    valid_subsidiaries = ['AMS', 'ACS', 'ASS', 'APS', 'ATI']
    return value in valid_subsidiaries

def validate_transaction_type(value):
    valid_transaction_types = ['cash', 'upi', 'bank_transfer']
    return value in valid_transaction_types

@csrf_exempt
def create_transaction(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            # Customize error response format
            errors = {}
            for field, messages in serializer.errors.items():
                errors[field] = messages[0]
            return JsonResponse(errors, status=400)

def get_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    transaction_data = {
        'transaction_id': transaction.transaction_id,
        'receiver_name': transaction.receiver_name,
        'receiver_id': transaction.receiver_id,
        'sender_name': transaction.sender_name,
        'sender_id': transaction.sender_id,
        'accountant_name': transaction.accountant_name,
        'accountant_id': transaction.accountant_id,
        'credited_amount': str(transaction.credited_amount),
        'debited_amount': str(transaction.debited_amount),
        'transaction_datetime': transaction.transaction_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'uploaded_datetime': transaction.uploaded_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'transaction_type': transaction.transaction_type,
        'subsidiary': transaction.subsidiary,
        'currency': transaction.currency,
        'description': transaction.description,
    }
    return JsonResponse(transaction_data)

@csrf_exempt
def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        transaction.receiver_name = data.get('receiver_name', transaction.receiver_name)
        transaction.receiver_id = data.get('receiver_id', transaction.receiver_id)
        transaction.sender_name = data.get('sender_name', transaction.sender_name)
        transaction.sender_id = data.get('sender_id', transaction.sender_id)
        transaction.accountant_name = data.get('accountant_name', transaction.accountant_name)
        transaction.accountant_id = data.get('accountant_id', transaction.accountant_id)
        transaction.credited_amount = data.get('credited_amount', transaction.credited_amount)
        transaction.debited_amount = data.get('debited_amount', transaction.debited_amount)
        transaction.transaction_datetime = data.get('transaction_datetime', transaction.transaction_datetime)
        transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
        transaction.subsidiary = data.get('subsidiary', transaction.subsidiary)
        transaction.currency = data.get('currency', transaction.currency)
        transaction.description = data.get('description', transaction.description)
        transaction.save()

        return JsonResponse({'message': 'Transaction updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    if request.method == 'DELETE':
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_transactions(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        transaction_data = list(transactions.values())
        return JsonResponse(transaction_data, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
def get_transactions_by_fields(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        filters = {}

        # Extract fields from the request body
        receiver_id = data.get('receiver_id')
        sender_id = data.get('sender_id')
        accountant_id = data.get('accountant_id')

        # Build filter dictionary
        if receiver_id:
            filters['receiver_id'] = receiver_id
        if sender_id:
            filters['sender_id'] = sender_id
        if accountant_id:
            filters['accountant_id'] = accountant_id

        # Query transactions based on filters
        transactions = Transaction.objects.filter(**filters)

        # Convert queryset to list of dictionaries
        transaction_data = list(transactions.values())

        return JsonResponse(transaction_data, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt  # Use this decorator if you're testing without CSRF tokens
def transaction_date_range_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)

    try:
        body = json.loads(request.body)
        start_date = body.get('start_date')
        end_date = body.get('end_date')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    if not start_date or not end_date:
        return JsonResponse({'error': 'Both start_date and end_date are required.'}, status=400)

    try:
        # Parsing the dates to ensure they are valid
        start_date = parse_datetime(start_date)
        end_date = parse_datetime(end_date)
        if not start_date or not end_date:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format.'}, status=400)

    if start_date > end_date:
        return JsonResponse({'error': 'start_date must be before end_date.'}, status=400)

    # Filtering the transactions based on the date range
    transactions = Transaction.objects.filter(transaction_datetime__range=[start_date, end_date])
    
    # Serializing the queryset to a list of dictionaries
    transactions_data = list(transactions.values())

    return JsonResponse(transactions_data, safe=False, status=200)