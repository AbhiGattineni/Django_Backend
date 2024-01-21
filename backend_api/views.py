from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view
from .models import Person, AccessRoles, CollegesList, Consultant
from .serializers import PersonSerializer, CollegesListSerializer, ConsultantSerializer
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
import logging
from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand
import pandas as pd
logger = logging.getLogger(__name__)




@api_view(['POST'])
def create_person(request):
    if request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_person(request, pk):
    query_params = request.query_params
    print('Query Parameters:', query_params)
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    

class AddRoleView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        role = AccessRoles.objects.create(admin_access_role=data['admin_access_role'], name_of_role=data['name_of_role'])
        return JsonResponse({'id': role.id})

class GetRoleView(APIView):
    def get(self, request, role_id):
        try:
            role = AccessRoles.objects.get(id=role_id)
            return JsonResponse({'admin_access_role': role.admin_access_role, 'name_of_role': role.name_of_role})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)

class GetAllRolesView(APIView):
    def get(self, request):
        roles = AccessRoles.objects.all()
        roles_data = [{'id': role.id, 'admin_access_role': role.admin_access_role, 'name_of_role': role.name_of_role} for role in roles]
        return JsonResponse(roles_data, safe=False)

class UpdateRoleView(APIView):
    def put(self, request, role_id):
        data = json.loads(request.body)
        try:
            role = AccessRoles.objects.get(id=role_id)
            role.admin_access_role = data.get('admin_access_role', role.admin_access_role)
            role.name_of_role = data.get('name_of_role', role.name_of_role)
            role.save()
            return JsonResponse({'message': 'Role updated successfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)

class DeleteRoleView(APIView):
    def delete(self, request, role_id):
        try:
            role = AccessRoles.objects.get(id=role_id)
            role.delete()
            return JsonResponse({'message': 'Role deleted successfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)

class ConsultantCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = ConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_all_colleges(request):
    if request.method == 'GET':
        colleges = CollegesList.objects.all()
        serializer = CollegesListSerializer(colleges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_college(request):
    if request.method == 'POST':
        serializer = CollegesListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_college(request, pk):
    try:
        college = CollegesList.objects.get(pk=pk)
    except CollegesList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollegesListSerializer(college)
        return Response(serializer.data)

@api_view(['PUT'])
def update_college(request, pk):
    try:
        college = CollegesList.objects.get(pk=pk)
    except CollegesList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CollegesListSerializer(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_college(request, pk):
    try:
        college = CollegesList.objects.get(pk=pk)
    except CollegesList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        college.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConsultantListAPIView(APIView):
    def get(self, request, format=None):
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)

class ConsultantDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):
        # Use get_object_or_404 to simplify the code
        consultant = get_object_or_404(Consultant, pk=pk)

        try:
            consultant.delete()
            return Response({'message': 'Consultant deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Log the exception for debugging
            logger.error(f'Error deleting consultant with id {pk}: {e}')
            return Response({'error': 'Error occurred during deletion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsultantUpdateAPIView(APIView):
    def put(self, request, pk, format=None):
        # Handling the case where the consultant does not exist
        consultant = get_object_or_404(Consultant, pk=pk)

        serializer = ConsultantSerializer(consultant, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                # Handling invalid data
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Logging unexpected exceptions
            logger.error(f'Unexpected error occurred while updating consultant with id {pk}: {e}')
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


