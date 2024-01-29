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
from rest_framework import generics

from .models import Todo, Person, AccessRoles, CollegesList, Consultant, User, Role, PartTimer, Package
from .serializers import TodoSerializer, PersonSerializer, CollegesListSerializer, ConsultantSerializer, UserSerializer, AccessRolesSerializer, RoleSerializer, PartTimerSerializer, PackageSerializer

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
        user = User.objects.get(user_id=user_id)

        # Check if user has a related PartTimer entry with all questions answered as true
        part_timer_entry = PartTimer.objects.filter(user=user).first()
        if part_timer_entry and part_timer_entry.answered_questions:
            return Response({'message': 'User already exists and answered all questions', 'all_questions_answered': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User already exists but has not answered all questions', 'all_questions_answered': False}, status=status.HTTP_200_OK)

    # If user does not exist, create a new user
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#view to show all the user, roles, and assigned roles data.
@api_view(['GET'])
def user_data_and_roles_view(request):
    # Fetching all users
    users = User.objects.all()
    users_serializer = UserSerializer(users, many=True)

    # Fetching all roles
    roles = AccessRoles.objects.all()
    roles_serializer = AccessRolesSerializer(roles, many=True)

    # Fetching all assigned roles
    assigned_roles = Role.objects.all()
    assigned_roles_serializer = RoleSerializer(assigned_roles, many=True)

    # Combining all data in a single response
    combined_data = {
        'users': users_serializer.data,
        'roles': roles_serializer.data,
        'assigned_roles': assigned_roles_serializer.data,
    }
    return Response(combined_data, status=status.HTTP_200_OK)

# view to assign a role to a user
@api_view(['POST'])
def assign_role(request):
    print(request.data)
    try:
        user_id = request.data.get('user')
        role_id = request.data.get('role')
        print(user_id, role_id)
        # Fetch user name and role name
        try:
            user_name = User.objects.get(user_id=user_id).full_name
            role_name = AccessRoles.objects.get(id=role_id).name_of_role
        except (User.DoesNotExist, AccessRoles.DoesNotExist):
            return Response({'error': 'User or Role not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create and save new Role
        new_role = Role(user_id=user_id, name=user_name, role_name=role_name)
        new_role.save()

        return Response({'message': 'Role assigned successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Handle unexpected errors
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view to delete a assogned role
class DeleteUserAccessRoleView(APIView):
    def delete(self, request, role_id):
        try:
            role = Role.objects.get(pk=role_id)
            role.delete()
            return Response({'message': 'Role deleted successfully'}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_part_timer(request):
    try:
        # Extract user_id and email from the request
        user_id = request.data.get('user_id')
        email = request.data.get('email')
        
        # Check if a User with the given user_id and email exists
        user = User.objects.filter(user_id=user_id, email_id=email).first()

        if user:

            # Prepare and validate part-timer data
            part_timer_data = request.data.copy()
            part_timer_data['user'] = user.user_id  # Assign the User's user_id as the foreign key

            part_timer_serializer = PartTimerSerializer(data=part_timer_data)

            if part_timer_serializer.is_valid():
                part_timer_serializer.save()
                return Response(part_timer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Errors:", part_timer_serializer.errors)
                return Response(part_timer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User not found.")
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("An error occurred:", e)
        return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_part_timer(request, user_id):
    try:
        # Find the part-timer information based on the user_id
        part_timer = PartTimer.objects.filter(user=user_id).first()

        if part_timer:
            # Serialize the part-timer data
            part_timer_serializer = PartTimerSerializer(part_timer)
            return Response(part_timer_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Part-timer not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("An error occurred:", e)
        return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PackageListCreateView(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PackageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



