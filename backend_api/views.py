import json
import logging
import os
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AcsParttimerStatus
from .models import StatusUpdates
from .models import CollegeDetail
from .serializers import CollegeDetailSerializer
from rest_framework.parsers import JSONParser
from datetime import datetime
from django.utils.dateparse import parse_datetime

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import Todo, Person, AccessRoles, CollegesList, Consultant, User, Role, PartTimer, Package, ShopingProduct, Subsidiary
from .serializers import StatusUpdatesSerializer, TodoSerializer, PersonSerializer, CollegesListSerializer, ConsultantSerializer, UserSerializer, AccessRolesSerializer, RoleSerializer, PartTimerSerializer, PackageSerializer, ShopingProductSerializer,DeviceAllocationSerializer
from .serializers import SubsidiarySerializer

from rest_framework.generics import get_object_or_404
from .models import Employer, Recruiter, StatusConsultant, Consultant,DeviceAllocation
from .serializers import EmployerSerializer, RecruiterSerializer, StatusConsultantSerializer,StatusUpdatesSerializer,HappinessIndexSerializer

import fitz  # PyMuPDF
import docx

logger = logging.getLogger(__name__)

from .models import TeamMember,HappinessIndex
from .serializers import TeamMemberSerializer# View all team members
@api_view(['GET'])
def get_all_team_members(request):
    team_members = TeamMember.objects.all()
    serializer = TeamMemberSerializer(team_members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View a single team member by ID
@api_view(['GET'])
def get_single_team_member(request, pk):
    try:
        team_member = TeamMember.objects.get(pk=pk)
        serializer = TeamMemberSerializer(team_member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TeamMember.DoesNotExist:
        return Response({"error": "Team member not found"}, status=status.HTTP_404_NOT_FOUND)

# Add a new team member
@api_view(['POST'])
def add_team_member(request):
    serializer = TeamMemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a team member by ID
@api_view(['DELETE'])
def delete_team_member(request, pk):
    try:
        team_member = TeamMember.objects.get(pk=pk)
        team_member.delete()
        return Response({"message": "Team member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except TeamMember.DoesNotExist:
        return Response({"error": "Team member not found"}, status=status.HTTP_404_NOT_FOUND)

# Update a team member by ID
@api_view(['PUT'])
def update_team_member(request, pk):
    try:
        team_member = TeamMember.objects.get(pk=pk)
        serializer = TeamMemberSerializer(team_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except TeamMember.DoesNotExist:
        return Response({"error": "Team member not found"}, status=status.HTTP_404_NOT_FOUND)


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
            consultant = serializer.save()
            return Response({
                "consultant": ConsultantSerializer(consultant).data,
                "status_consultant": StatusConsultantSerializer(consultant.statusconsultant_set.first()).data if consultant.statusconsultant_set.exists() else None
            }, status=status.HTTP_201_CREATED)
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
        return Response({"error": "College not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollegesListSerializer(college)
        return Response(serializer.data)

@api_view(['PUT'])
def update_college(request, pk):
    try:
        college = CollegesList.objects.get(pk=pk)
    except CollegesList.DoesNotExist:
        return Response({"error": "College not found."}, status=status.HTTP_404_NOT_FOUND)

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
        return Response({"error": "College not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        college.delete()
        return Response({"message": "College successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

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
    user_id = request.data.get('user_id')
    
    # Check if user already exists
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
            # Update only the empty or null fields
            update_data = {field: value for field, value in request.data.items() if not getattr(user, field, None)}
            serializer = UserSerializer(user, data=update_data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                empty_fields = [field.name for field in user._meta.fields if not getattr(user, field.name, None)]
                
                if not empty_fields:
                    # Filter roles based on user_id
                    assigned_roles = Role.objects.filter(user_id=user_id)
                    assigned_roles_serializer = RoleSerializer(assigned_roles, many=True)
                    roles = [role['role_name'] for role in assigned_roles_serializer.data]
                    
                    return Response({
                        'empty_fields': empty_fields,
                        'roles': roles
                    }, status=status.HTTP_200_OK)
                
                return Response({
                    'empty_fields': empty_fields
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass  # If user does not exist, we'll create a new one
    
    # Create a new user if it doesn't exist
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        empty_fields = [field.name for field in user._meta.fields if not getattr(user, field.name, None)]
        
        if not empty_fields:
            # Filter roles based on user_id
            assigned_roles = Role.objects.filter(user_id=user_id)
            assigned_roles_serializer = RoleSerializer(assigned_roles, many=True)
            roles = [role['role_name'] for role in assigned_roles_serializer.data]
            
            return Response({
                'empty_fields': empty_fields,
                'roles': roles
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'empty_fields': empty_fields
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#view to show all the user, roles, and assigned roles data.
@api_view(['GET'])
def user_data_and_roles_view(request):
    # Construct a dictionary with request details
    request_data = {
        'method': request.method,
        'path': request.get_full_path(),
        'headers': dict(request.headers),
        'body': request.body.decode('utf-8', errors='replace') if request.body else ''
    }

    # Serialize the dictionary to a JSON-formatted string
    request_json = json.dumps(request_data, indent=4)

    # Print the JSON string
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
    try:
        user_id = request.data.get('user')
        role_id = request.data.get('role')
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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("An error occurred:", e)
        return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_part_timer(request, user_id):
    try:
        # Find the part-timer information based on the user_id
        user = User.objects.get(user_id=user_id)

        if user:
            # Serialize the part-timer data
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
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


@api_view(['GET'])
@csrf_exempt
def acsParttimerStatus_detail(request, parttimer_id):
    try:
        applications = AcsParttimerStatus.objects.filter(parttimerId=parttimer_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "No applications found for this parttimerId"}, status=404)
    if request.method == "GET":
        data = []
        for application in applications:
            data.append({
                "parttimerName": application.parttimerName,
                "parttimerId": application.parttimerId,
                "studentName": application.studentName,
                "studentId": application.studentId,
                "date": application.date,
                "applicationsAppliedSearched": application.applicationsAppliedSearched,
                "applicationsAppliedSaved": application.applicationsAppliedSaved,
                "easyApply": application.easyApply,
                "recruiterDirectMessages": application.recruiterDirectMessages,
                "connectMessages": application.connectMessages,
                "reason": application.reason,
                "description": application.description
            })
        return JsonResponse(data, safe=False)

@api_view(['POST'])
@csrf_exempt
def acsParttimerStatus_create(request):
    try:
        if request.method == "POST":
            data = request.data  # Use request.data for JSON data
            
            try:
                # Validate date to ensure it's not in the future
                if data.get("date"):
                    date_value = timezone.make_aware(timezone.datetime.strptime(data["date"], "%Y-%m-%d"))
                    if date_value > timezone.now():
                        return JsonResponse({"message": "Date cannot be in the future"}, status=400)
                
                # Check if there's an existing record with the same studentId, parttimerId, and date
                existing_application = AcsParttimerStatus.objects.filter(
                    studentId=data["studentId"],
                    parttimerId=data["parttimerId"],
                    date=data["date"]
                ).first()
                
                if existing_application:
                    return JsonResponse({"message": "Already submitted..!"}, status=400)
                
                # Create a new AcsParttimerStatus object
                application = AcsParttimerStatus.objects.create(
                    parttimerName=data["parttimerName"],
                    parttimerId=data["parttimerId"],
                    studentName=data["studentName"],
                    studentId=data["studentId"],
                    date=data["date"],
                    applicationsAppliedSearched=data.get("applicationsAppliedSearched", 0),
                    applicationsAppliedSaved=data.get("applicationsAppliedSaved", 0),
                    easyApply=data.get("easyApply", 0),
                    recruiterDirectMessages=data.get("recruiterDirectMessages", ""),
                    connectMessages=data.get("connectMessages", ""),
                    reason=data.get("reason", ""),
                    description=data.get("description", "")
                )
                
                return JsonResponse({"message": "Status saved successfully"})
            
            except KeyError as e:
                field = e.args[0]
                return JsonResponse({"message": f"{field} required field is missing"}, status=400)
            
            except Exception as e:
                return JsonResponse({"message": "Something went wrong! Try again."}, status=500)
        
    except Exception as e:
        return JsonResponse({"message": "Something went wrong! Try again."}, status=500)


@api_view(['PUT'])
@csrf_exempt
def acsParttimerStatus_update(request):
    try:
        if request.method == "PUT":
            data = request.data  # Use request.data for JSON data
            
            try:
                # Check if there's an existing record with the same studentId, parttimerId, and date
                existing_application = AcsParttimerStatus.objects.filter(
                    studentId=data["studentId"],
                    parttimerId=data["parttimerId"],
                    date=data["date"]
                ).first()
                
                if existing_application:
                    # Update existing application
                    existing_application.parttimerName = data["parttimerName"]
                    existing_application.studentName = data["studentName"]
                    existing_application.applicationsAppliedSearched = data.get("applicationsAppliedSearched", 0)
                    existing_application.applicationsAppliedSaved = data.get("applicationsAppliedSaved", 0)
                    existing_application.easyApply = data.get("easyApply", 0)
                    existing_application.recruiterDirectMessages = data.get("recruiterDirectMessages", "")
                    existing_application.connectMessages = data.get("connectMessages", "")
                    existing_application.reason = data.get("reason", "")
                    existing_application.description = data.get("description", "")
                    existing_application.save()
                    
                    return JsonResponse({"message": "Status updated successfully"})
                else:
                    return JsonResponse({"message": "No record found to update"}, status=404)
            
            except KeyError as e:
                field = e.args[0]
                return JsonResponse({"message": f"{field} required field is missing"}, status=400)
            
            except Exception as e:
                return JsonResponse({"message": "An error occurred"}, status=500)
        
    except Exception as e:
        return JsonResponse({"message": "An error occurred"}, status=500)

@api_view(['DELETE'])
@csrf_exempt
def acsParttimerStatus_delete(request):
    try:
        data = request.data  # Use request.data for JSON data
        
        # Check if there's an existing record with the provided criteria
        existing_application = AcsParttimerStatus.objects.filter(
            studentId=data["studentId"],
            parttimerId=data["parttimerId"],
            date=data["date"]
        ).first()
        
        if existing_application:
            existing_application.delete()
            return JsonResponse({"message": "Application deleted successfully"}, status=204)
        else:
            return JsonResponse({"error": "Application not found"}, status=404)
        
    except KeyError as e:
        field = e.args[0]
        return JsonResponse({"error": f"{field} required field is missing"}, status=400)
    except Exception as e:
        return JsonResponse({"error": "An error occurred"}, status=500)

@api_view(['GET'])
@csrf_exempt
def application_list(request):
    if request.method == "GET":
        applications = AcsParttimerStatus.objects.all()
        data = []
        for application in applications:
            data.append({
                "parttimerName": application.parttimerName,
                "parttimerId": application.parttimerId,
                "studentName": application.studentName,
                "studentId": application.studentId,
                "date": application.date,
                "applicationsAppliedSearched": application.applicationsAppliedSearched,
                "applicationsAppliedSaved": application.applicationsAppliedSaved,
                "easyApply": application.easyApply,
                "recruiterDirectMessages": application.recruiterDirectMessages,
                "connectMessages": application.connectMessages,
                "reason": application.reason,
                "description": application.description,
            })
        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
def application_detail_by_id_and_date(request, id, date):
    try:
        # Convert date string to datetime object
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Retrieve all applications based on parttimerId and date
        applications = AcsParttimerStatus.objects.filter(parttimerId=id, date=date_obj)
        
        # Check if any applications are found
        if applications.exists():
            # Create a list to store application details
            application_details = []
            for application in applications:
                # Append application details to the list
                application_details.append({
                    "parttimerName": application.parttimerName,
                    "parttimerId": application.parttimerId,
                    "studentName": application.studentName,
                    "studentId": application.studentId,
                    "date": application.date,
                    "applicationsAppliedSearched": application.applicationsAppliedSearched,
                    "applicationsAppliedSaved": application.applicationsAppliedSaved,
                    "easyApply": application.easyApply,
                    "recruiterDirectMessages": application.recruiterDirectMessages,
                    "connectMessages": application.connectMessages,
                    "reason": application.reason,
                    "description": application.description
                })
            
            # Return the list of application details as JSON response
            return JsonResponse(application_details, safe=False)
        else:
            return JsonResponse({"error": "No applications found for the given parttimerId and date"}, status=404)
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Please use 'YYYY-MM-DD'."}, status=400)
    
from django.db.models import Min
# Status Updates
@api_view(['GET'])
@csrf_exempt
def get_status_ids(request):
    if request.method == 'GET':
        # Get unique user_id and the first occurrence of user_name
        unique_users = StatusUpdates.objects.values('user_id').annotate(user_name=Min('user_name'))
        
        # Return as an array of dictionaries
        return JsonResponse(list(unique_users), safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import StatusUpdates
from datetime import datetime, timedelta

@api_view(['POST'])
@csrf_exempt
def create_status(request):
    try:
        if request.method == "POST":
            data = request.data

            try:
                # Validate date to ensure it's not in the future
                if "date" in data and data["date"]:
                    date_value = timezone.datetime.strptime(data["date"], "%Y-%m-%d").date()
                    if date_value > timezone.localdate():
                        return JsonResponse({"message": "Date cannot be in the future"}, status=400)

                user_id = data.get("user_id")
                if not user_id:
                    return JsonResponse({"message": "user_id is required"}, status=400)

                # Check if there's an existing record with the same user_id, subsidiary, and date
                existing_status = StatusUpdates.objects.filter(
                    user_id=user_id,
                    date=data.get("date"),
                    subsidary=data.get("subsidary")
                ).first()
                
                if existing_status:
                    return JsonResponse({"message": "Already submitted..!"}, status=400)

                # Get user_name from the request or fetch full_name from User model
                user_name = data.get("user_name")
                if not user_name:
                    try:
                        user = User.objects.get(user_id=user_id)
                        user_name = user.full_name
                    except User.DoesNotExist:
                        return JsonResponse({"message": "User not found for the given user_id"}, status=400)

                # Handle multiple dates if this is a leave request
                dates_to_create = []
                start_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
                
                if data.get("leave") and data.get("endDate"):
                    end_date = datetime.strptime(data["endDate"], "%Y-%m-%d").date()
                    current_date = start_date
                    while current_date <= end_date:
                        dates_to_create.append(current_date)
                        current_date += timedelta(days=1)
                else:
                    dates_to_create = [start_date]

                # Create status records for all dates
                for status_date in dates_to_create:
                    StatusUpdates.objects.create(
                        user_id=user_id,
                        user_name=user_name,
                        subsidary=data["subsidary"],
                        source=data.get("source", None),
                        date=status_date,
                    description=data.get("description", None),
                    studentName=data.get("studentName", None),
                    whatsappId=data.get("whatsappId", None),
                    applicationsAppliedSearched=data.get("applicationsAppliedSearched", 0),
                    applicationsAppliedSaved=data.get("applicationsAppliedSaved", 0),
                    easyApply=data.get("easyApply", 0),
                    recruiterDirectMessages=data.get("recruiterDirectMessages", None),
                    connectMessages=data.get("connectMessages", None),
                    reason=data.get("reason", None),
                    ticket_link=data.get("ticket_link", None),
                    github_link=data.get("github_link", None),
                    account_name=data.get("account_name", None),
                    stock_name=data.get("stock_name", None),
                    stock_quantity=data.get("stock_quantity", None),
                    stock_value=data.get("stock_value", None),
                    transaction_type=data.get("transaction_type", None),
                    total_current_amount=data.get("total_current_amount", None),
                    pickup_location=data.get("pickup_location", None),
                    pickup_contact=data.get("pickup_contact", None),
                    dropoff_location=data.get("dropoff_location", None),
                    dropoff_contact=data.get("dropoff_contact", None),
                    distance_travelled=data.get("distance_travelled", None),
                    whatsapp_group_number=data.get("whatsapp_group_number", None),
                    leave=data.get("leave", None)
                )
                
                # Return success message with number of dates created
                num_dates = len(dates_to_create)
                message = f"Status{'es' if num_dates > 1 else ''} saved successfully for {num_dates} day{'s' if num_dates > 1 else ''}"
                return JsonResponse({"message": message}, status=201)
            
            except KeyError as e:
                field = e.args[0]
                return JsonResponse({"message": f"{field} required field is missing"}, status=400)
            
            except Exception as e:
                return JsonResponse({"message": "Something went wrong! Try again."}, status=500)
    
    except Exception as e:
        return JsonResponse({"message": "Something went wrong!"}, status=500)
    
@api_view(['POST'])
@csrf_exempt
def get_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    filters = {}
    user_id = data.get("user_id")
    date = data.get("date")
    if user_id:
        filters['user_id'] = user_id
    if date:
        filters['date'] = date

    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if start_date and end_date:
        try:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            if not start_date or not end_date:
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format.'}, status=400)

        if start_date > end_date:
            return JsonResponse({'error': 'start_date must be before end_date.'}, status=400)

        filters['date__range'] = [start_date, end_date]

    status = StatusUpdates.objects.filter(**filters)
    status_data = list(status.values())
    return JsonResponse(status_data, safe=False, status=200)

@api_view(['PUT'])
@csrf_exempt
def update_status_by_id(request):
    try:
        if request.method == "PUT":
            data = request.data
            existing_application = StatusUpdates.objects.filter(
                user_id=data.get("user_id"),
                date=data.get("date"),
                subsidary=data.get("subsidary")
            ).first()
            
            if existing_application:
                for key, value in data.items():
                    if hasattr(existing_application, key) and value is not None:
                        setattr(existing_application, key, value)
                existing_application.save()
                return JsonResponse({"message": "Status updated successfully"})
            else:
                return JsonResponse({"message": "No record found to update"}, status=404)
    except KeyError as e:
        return JsonResponse({"message": f"{e.args[0]} required field is missing"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An error occurred"}, status=500)

@api_view(['DELETE'])
@csrf_exempt
def delete_status_by_id(request):
    try:
        data = request.data
        existing_application = StatusUpdates.objects.filter(
            user_id=data.get("user_id"),
            date=data.get("date")
        ).first()
        
        if existing_application:
            existing_application.delete()
            return JsonResponse({"message": "Application deleted successfully"}, status=204)
        else:
            return JsonResponse({"error": "Application not found"}, status=404)
    except KeyError as e:
        return JsonResponse({"error": f"{e.args[0]} required field is missing"}, status=400)
    except Exception as e:
        return JsonResponse({"error": "An error occurred"}, status=500)

@api_view(['GET'])
def get_college_details(request):
    if request.method == 'GET':
        college_details = CollegeDetail.objects.all()
        serializer = CollegeDetailSerializer(college_details, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def college_detail_view(request):
    filters = {}

    try:
        college_id = request.GET.get('college')
        if college_id:
            try:
                filters['college__id'] = int(college_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid college ID'}, status=400)
        
        college_name = request.GET.get('college_name')
        if college_name:
            filters['college_name__icontains'] = college_name
        
        label = request.GET.get('label')
        if label:
            filters['label__icontains'] = label
        
        link = request.GET.get('link')
        if link:
            filters['link__icontains'] = link

        college_details = CollegeDetail.objects.filter(**filters)
        response_data = [
            {
                'college_id': detail.college.id,
                'college_name': detail.college_name,
                'label': detail.label,
                'link': detail.link,
            }
            for detail in college_details
        ]

        return JsonResponse(response_data, safe=False)
    
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'College not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def create_college_detail(request):
    if request.method == 'POST':
        serializer = CollegeDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_college_detail(request, pk):
    try:
        college_detail = get_object_or_404(CollegeDetail, pk=pk)
        serializer = CollegeDetailSerializer(college_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CollegeDetail.DoesNotExist:
        return Response({'error': 'CollegeDetail not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_college_detail(request, pk):
    try:
        college_detail = get_object_or_404(CollegeDetail, pk=pk)
        college_detail.delete()
        return Response({'message': 'CollegeDetail successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    except CollegeDetail.DoesNotExist:
        return Response({'error': 'CollegeDetail not found'}, status=status.HTTP_404_NOT_FOUND)
    
# Fetch all products
@api_view(['GET'])
def get_all_products(request):
    products = ShopingProduct.objects.all()
    serializer = ShopingProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Fetch a single product by its id
@api_view(['GET'])
def get_single_product(request, pk):
    try:
        product = ShopingProduct.objects.get(pk=pk)
        serializer = ShopingProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ShopingProduct.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
# Add a new product
@api_view(['POST'])
def add_product(request):
    serializer = ShopingProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = ShopingProduct.objects.get(pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ShopingProduct.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = ShopingProduct.objects.get(pk=pk)
        serializer = ShopingProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ShopingProduct.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# Employer Views
class EmployerListCreateAPIView(APIView):
    def get(self, request):
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        employer = get_object_or_404(Employer, pk=pk)
        serializer = EmployerSerializer(employer)
        return Response(serializer.data)

    def put(self, request, pk):
        employer = get_object_or_404(Employer, pk=pk)
        serializer = EmployerSerializer(employer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employer = get_object_or_404(Employer, pk=pk)
        employer.delete()
        
        # Return success message
        return Response({"message": "Employer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Recruiter Views
class RecruiterListCreateAPIView(APIView):
    def get(self, request):
        recruiters = Recruiter.objects.all()
        serializer = RecruiterSerializer(recruiters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecruiterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        recruiter = get_object_or_404(Recruiter, pk=pk)
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)

    def put(self, request, pk):
        recruiter = get_object_or_404(Recruiter, pk=pk)
        serializer = RecruiterSerializer(recruiter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recruiter = get_object_or_404(Recruiter, pk=pk)
        recruiter.delete()
        return Response({"message": "Recruiter deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# StatusConsultant Views
class StatusConsultantListCreateAPIView(APIView):
    def get(self, request):
        status_consultants = StatusConsultant.objects.all()
        serializer = StatusConsultantSerializer(status_consultants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StatusConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusConsultantRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        status_consultant = get_object_or_404(StatusConsultant, pk=pk)
        serializer = StatusConsultantSerializer(status_consultant)
        return Response(serializer.data)

    def put(self, request, pk):
        status_consultant = get_object_or_404(StatusConsultant, pk=pk)
        serializer = StatusConsultantSerializer(status_consultant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        status_consultant = get_object_or_404(StatusConsultant, pk=pk)
        status_consultant.delete()
        return Response({"message": "Status deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


def health_check(request):
    return JsonResponse({'status': 'ok'})



# Get all device allocations
@api_view(['GET'])
def get_all_devices(request):
    devices = DeviceAllocation.objects.all()
    serializer = DeviceAllocationSerializer(devices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get a single device allocation by ID
@api_view(['GET'])
def get_single_device(request, pk):
    try:
        device = DeviceAllocation.objects.get(pk=pk)
        serializer = DeviceAllocationSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DeviceAllocation.DoesNotExist:
        return Response({"error": "Device allocation not found"}, status=status.HTTP_404_NOT_FOUND)

# Add a new device allocation
@api_view(['POST'])
def add_device(request):
    serializer = DeviceAllocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update an existing device allocation
@api_view(['PUT'])
def update_device(request, pk):
    try:
        device = DeviceAllocation.objects.get(pk=pk)
        serializer = DeviceAllocationSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except DeviceAllocation.DoesNotExist:
        return Response({"error": "Device allocation not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete a device allocation
@api_view(['DELETE'])
def delete_device(request, pk):
    try:
        device = DeviceAllocation.objects.get(pk=pk)
        device.delete()
        return Response({"message": "Device allocation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except DeviceAllocation.DoesNotExist:
        return Response({"error": "Device allocation not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@csrf_exempt
def get_status_by_id(request, user_id):
    if request.method == 'GET':
        try:
            status_queryset = StatusUpdates.objects.filter(user_id=user_id)
            status_data = list(status_queryset.values())

            # Use timezone-aware date
            today = timezone.now().date()
            has_submitted = HappinessIndex.objects.filter(
                employee_id=user_id, 
                date=today
            ).exists()

            response_data = {
                'status_updates': status_data,
                'has_submitted_happiness_today': has_submitted
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse(
                {'message': 'Error processing request: ' + str(e)}, 
                status=500
            )
    else:
        return JsonResponse(
            {'message': 'Invalid request method'}, 
            status=405
        )

@api_view(['POST'])
def submit_happiness_index(request, user_id):
    try:
        # Fetch the user object using the user_id (from get_user_by_id call)
        user = User.objects.get(user_id=user_id)

        # Check if the employee has already submitted happiness for today
        today = timezone.now().date()
        has_submitted = HappinessIndex.objects.filter(employee=user, date=today).exists()

        if has_submitted:
            return Response(
                {"message": "You have already submitted your happiness index for today."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # If they haven't submitted, proceed to save the happiness index
        happiness_score = request.data.get('happiness_score')
        description = request.data.get('description', '')

        # Create new HappinessIndex instance
        happiness_index = HappinessIndex.objects.create(
            employee=user,
            happiness_score=happiness_score,
            description=description,
            date=today
        )

        # Serialize the data to return a response
        serializer = HappinessIndexSerializer(happiness_index)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_happiness_index(request,user_id):
    try:
        # Fetch the user object using the user_id (from get_user_by_id call)
        user = User.objects.get(user_id=user_id)
        
        # Retrieve all the happiness index records for this employee
        happiness_indexes = HappinessIndex.objects.filter(employee=user)
        
        # If there are no records, return a message
        if not happiness_indexes:
            return Response({"message": "No happiness index records found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the happiness indexes
        serializer = HappinessIndexSerializer(happiness_indexes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_happiness_indexes(request):
    try:
        # Retrieve all happiness index records from the database
        happiness_indexes = HappinessIndex.objects.all()

        # If no records are found, return a message
        if not happiness_indexes:
            return Response({"message": "No happiness index records found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the happiness indexes
        serializer = HappinessIndexSerializer(happiness_indexes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class HappinessIndexListView(generics.ListAPIView):
    queryset = HappinessIndex.objects.select_related('employee').all()
    serializer_class = HappinessIndexSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join([page.get_text() for page in doc])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

@api_view(['POST'])
def parse_resume(request):
    file = request.FILES.get('resume')

    if not file:
        return Response({'error': 'No file uploaded'}, status=400)

    if file.name.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        text = extract_text_from_docx(file)
    else:
        return Response({'error': 'Unsupported file format'}, status=400)

    return Response(text)
@csrf_exempt
def get_default_words(request):
    # Path to your JSON file
    JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'defaultWords.json')
    if request.method == 'GET':
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
        return JsonResponse(data, safe=False)

    elif request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            with open(JSON_FILE_PATH, 'w') as f:
                json.dump(data, f, indent=2)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response({"message":"Only GET and POST/PUT allowed"})

@api_view(['GET'])
def get_all_subsidiaries(request):
    subsidiaries = Subsidiary.objects.all()
    serializer = SubsidiarySerializer(subsidiaries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_single_subsidiary(request, pk):
    try:
        subsidiary = Subsidiary.objects.get(pk=pk)
        serializer = SubsidiarySerializer(subsidiary)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Subsidiary.DoesNotExist:
        return Response({"error": "Subsidiary not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_subsidiary(request):
    serializer = SubsidiarySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_subsidiary(request, pk):
    try:
        subsidiary = Subsidiary.objects.get(pk=pk)
        serializer = SubsidiarySerializer(subsidiary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Subsidiary.DoesNotExist:
        return Response({"error": "Subsidiary not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_subsidiary(request, pk):
    try:
        subsidiary = Subsidiary.objects.get(pk=pk)
        subsidiary.delete()
        return Response({"message": "Subsidiary deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Subsidiary.DoesNotExist:
        return Response({"error": "Subsidiary not found"}, status=status.HTTP_404_NOT_FOUND)
