from rest_framework import serializers
from .models import Todo
from .models import Person
from .models import Consultant
from .models import CollegesList
from .models import Consultant
from .models import User, PartTimer
from .models import AccessRoles
from .models import Role
from .models import Package
from .models import AcsParttimerStatus
from .models import StatusUpdates
from .models import CollegeDetail, ShopingProduct
from .models import StatusConsultant, Employer, Recruiter, Consultant
from .models import DeviceAllocation
from .models import HappinessIndex
import json
from django.utils import timezone

from .models import TeamMember
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'

class CollegesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegesList
        fields = '__all__'

class StatusConsultantSerializer(serializers.ModelSerializer):
    consultant_id = serializers.PrimaryKeyRelatedField(queryset=Consultant.objects.all(), required=False)
    recruiter_id = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all())
    employer_id = serializers.PrimaryKeyRelatedField(queryset=Employer.objects.all())

    class Meta:
        model = StatusConsultant
        fields = '__all__'

class ConsultantSerializer(serializers.ModelSerializer):
    status_consultant = StatusConsultantSerializer(required=False)

    class Meta:
        model = Consultant
        fields = '__all__'

    def to_internal_value(self, data):
        """Convert empty strings to None for specific fields."""
        fields_to_clean = [
            'consulting_resume',
            'original_resume',
            'btech_graduation_date',
            'masters_graduation_date',
            'visa_validity',
            'uploaded_date',
        ]
        for field in fields_to_clean:
            if field in data and data[field] == "":
                data[field] = None

        status_data = data.get('status_consultant', None)
        validated_data = super().to_internal_value(data)
        if status_data:
            validated_data['status_consultant'] = status_data
        return validated_data

    def create(self, validated_data):
        status_data = validated_data.pop('status_consultant', None)
        consulting_resume = validated_data.pop('consulting_resume', None)
        original_resume = validated_data.pop('original_resume', None)
        btech_graduation_date = validated_data.pop('btech_graduation_date', None)
        masters_graduation_date = validated_data.pop('masters_graduation_date', None)

        # Create the Consultant instance
        consultant = Consultant.objects.create(**validated_data)

        # Assign files if provided
        if consulting_resume:
            consultant.consulting_resume = consulting_resume
        if original_resume:
            consultant.original_resume = original_resume
        if btech_graduation_date:
            consultant.btech_graduation_date = btech_graduation_date
        if masters_graduation_date:
            consultant.masters_graduation_date = masters_graduation_date
        consultant.save()

        if isinstance(status_data, str):
            status_data = json.loads(status_data)
        # Handle status_consultant if data exists
        if status_data["description"]:
            try:
                recruiter = Recruiter.objects.get(id=status_data['recruiter_id'])
                employer = Employer.objects.get(id=status_data['employer_id'])
                if status_data["date"] == "":
                    status_data["date"] = timezone.localdate()

                StatusConsultant.objects.create(
                    consultant_id=consultant,
                    recruiter_id=recruiter,
                    employer_id=employer,
                    date=status_data.get('date'),
                    description=status_data.get('description')
                )
            except (Recruiter.DoesNotExist, Employer.DoesNotExist):
                # Skipping validation here; just log or handle as needed.
                pass

        return consultant

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'required': True},
            'phone_country_code': {'required': False},
            'phone_number': {'required': False},
            'enrolled_services': {'required': False}
        }

class AccessRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoles
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PartTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTimer
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class AcsParttimerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcsParttimerStatus
        fields = '__all__'

from rest_framework import serializers
from .models import StatusUpdates, HappinessIndex

class CollegeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDetail
        fields = '__all__'

class ShopingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopingProduct
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class DeviceAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceAllocation
        fields = '__all__'


class StatusUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdates
        fields = '__all__'

class HappinessIndexSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = HappinessIndex
        fields = ['id', 'employee', 'happiness_score', 'description', 'date', 'full_name']

    def get_full_name(self, obj):
        return obj.employee.full_name 
