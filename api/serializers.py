from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id',
                  'date_task',
                  'time_task',
                  'text_task',
                  'address_task',
                  'author_task',
                  'employee_task',
                  'line_task',
                  'status_task',
                  'user']
