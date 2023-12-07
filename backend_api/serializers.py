from rest_framework import serializers
from .models import Todo
from .models import Person

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'