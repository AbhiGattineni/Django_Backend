import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo, Person, AccessRoles, CollegesList, Consultant, User
from .serializers import TodoSerializer, PersonSerializer, CollegesListSerializer, ConsultantSerializer, UserSerializer

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

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
        def get(self, request, todo_id, *args, **kwargs):

            todo_instance = self.get_object(todo_id, request.user.id)
            if not todo_instance:
                return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
        def put(self, request, todo_id, *args, **kwargs):
            '''
            Updates the todo item with given todo_id if exists
            '''
            todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
        def delete(self, request, todo_id, *args, **kwargs):
            '''
            Deletes the todo item with given todo_id if exists
            '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
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

@api_view(['POST'])
def log_first_time_user(request):
    # Check if user already exists
    user_id = request.data.get('user_id')
    if user_id and User.objects.filter(user_id=user_id).exists():
        return Response({'message': 'User already exists'}, status=status.HTTP_200_OK)

    # If user does not exist, create a new user
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)