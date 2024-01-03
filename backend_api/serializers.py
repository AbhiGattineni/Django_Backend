from rest_framework import serializers
from .models import Todo
from .models import Person
from .models import Consultant
from .models import CollegesList
from .models import Consultant

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
