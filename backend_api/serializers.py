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
class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
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