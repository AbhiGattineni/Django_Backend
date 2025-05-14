from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services.parser import parse_transactions
from .services.categorizer import TransactionCategorizer

@method_decorator(csrf_exempt, name='dispatch')
class UploadStatementView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES.get('statement')
        persist = request.data.get('persist', False)
        file_type = request.data.get('file_type', 'csv')

        if not file:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith(('.csv', '.pdf')):
            return Response({'error': 'Only CSV and PDF files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transactions = parse_transactions(file, file_type)
            if not transactions:
                return Response({'error': 'No valid transactions found in the file.'}, status=status.HTTP_400_BAD_REQUEST)

            # Categorize transactions
            categorizer = TransactionCategorizer()
            categorized_transactions = categorizer.categorize_transactions(transactions)

            # Optional: store transactions if user selected "persist"
            if persist:
                # TODO: Save to DB in future phase
                pass

            return Response({
                'message': 'Parsed successfully',
                'count': len(categorized_transactions),
                'file_type': file_type,
                'transactions': categorized_transactions
            })
        except Exception as e:
            return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


