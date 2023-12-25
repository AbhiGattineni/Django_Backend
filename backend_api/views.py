from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer
from .models import Person
from .serializers import PersonSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import AccessRoles
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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

@csrf_exempt
@require_http_methods(["POST"])
def add_role(request):
    data = json.loads(request.body)
    role = AccessRoles.objects.create(admin_access_role=data['admin_access_role'], name_of_role=data['name_of_role'])
    return JsonResponse({'id': role.id})

@require_http_methods(["GET"])
def get_role(request, role_id):
    try:
        role = AccessRoles.objects.get(id=role_id)
        return JsonResponse({'admin_access_role': role.admin_access_role, 'name_of_role': role.name_of_role})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)
def get_all_roles(request):
    roles = AccessRoles.objects.all()
    roles_data = [{'id': role.id, 'admin_access_role': role.admin_access_role, 'name_of_role': role.name_of_role} for role in roles]
    return JsonResponse(roles_data, safe=False)

@csrf_exempt
@require_http_methods(["PUT"])
def update_role(request, role_id):
    print(request.body)
    data = json.loads(request.body)
    try:
        role = AccessRoles.objects.get(id=role_id)
        role.admin_access_role = data.get('admin_access_role', role.admin_access_role)
        role.name_of_role = data.get('name_of_role', role.name_of_role)
        role.save()
        return JsonResponse({'message': 'Role updated successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_role(request, role_id):
    try:
        role = AccessRoles.objects.get(id=role_id)
        role.delete()
        return JsonResponse({'message': 'Role deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)