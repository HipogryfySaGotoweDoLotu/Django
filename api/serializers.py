from rest_framework import serializers
from .models import User, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'desc', 'created_at', 'updated_at', 'user']

class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'token', 'created_at', 'tasks']
