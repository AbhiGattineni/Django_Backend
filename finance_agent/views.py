from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services.parser import parse_transactions
from .services.categorizer import TransactionCategorizer
from .services.card_recommender import calculate_spending_summary, get_card_recommendation
from .services.card_extractor import get_current_cards

@method_decorator(csrf_exempt, name='dispatch')
class UploadStatementView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        files = request.FILES.getlist('statement')
        persist = request.data.get('persist', False)

        if not files:
            return Response({'error': 'No files uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        all_transactions = []
        file_results = []

        for file in files:
            if not file.name.endswith(('.csv', '.pdf')):
                file_results.append({
                    'filename': file.name,
                    'status': 'error',
                    'error': 'Only CSV and PDF files are allowed.'
                })
                continue

            try:
                file_type = 'pdf' if file.name.endswith('.pdf') else 'csv'
                transactions = parse_transactions(file, file_type)
                
                if not transactions:
                    file_results.append({
                        'filename': file.name,
                        'status': 'error',
                        'error': 'No valid transactions found in the file.'
                    })
                    continue

                # Categorize transactions
                categorizer = TransactionCategorizer()
                categorized_transactions = categorizer.categorize_transactions(transactions)
                
                all_transactions.extend(categorized_transactions)
                
                file_results.append({
                    'filename': file.name,
                    'status': 'success',
                    'count': len(categorized_transactions),
                    'file_type': file_type
                })

            except Exception as e:
                file_results.append({
                    'filename': file.name,
                    'status': 'error',
                    'error': str(e)
                })

        # Calculate spending summary and get card recommendations
        print(all_transactions)
        spending_summary = calculate_spending_summary(all_transactions)
        current_cards = get_current_cards(all_transactions)  # Extract cards from transactions
        card_suggestions = get_card_recommendation(spending_summary, current_cards)

        # Optional: store transactions if user selected "persist"
        if persist and all_transactions:
            # TODO: Save to DB in future phase
            pass

        return Response({
            'message': 'Processing completed',
            'total_count': len(all_transactions),
            'file_results': file_results,
            'transactions': all_transactions,
            'spending_summary': spending_summary,
            'current_cards': current_cards,  # Include detected cards in response
            'card_suggestions': card_suggestions
        })


