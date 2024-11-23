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
import json

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
        """Handle nested writable serializer data for status_consultant."""
        status_data = data.get('status_consultant', None)
        validated_data = super().to_internal_value(data)
        if status_data:
            validated_data['status_consultant'] = status_data
        return validated_data

    def create(self, validated_data):
        status_data = validated_data.pop('status_consultant', None)
        consultant = Consultant.objects.create(**validated_data)

        # Ensure status_data is a dictionary
        if isinstance(status_data, str):
            status_data = json.loads(status_data)

        if status_data:
            # Retrieve instances for foreign key fields
            recruiter = Recruiter.objects.get(id=status_data['recruiter_id'])
            employer = Employer.objects.get(id=status_data['employer_id'])

            # Create StatusConsultant with related instances
            StatusConsultant.objects.create(
                consultant_id=consultant,
                recruiter_id=recruiter,
                employer_id=employer,
                date=status_data.get('date'),
                description=status_data.get('description')
            )

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

class StatusUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdates
        fields = '__all__'

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
