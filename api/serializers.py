from rest_framework import serializers

from employee.models import Department, Position, Profile
from task.models import Task
from work_task.models import WorkTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = \
            [
                'id',
                'date_task',
                'time_task',
                'text_task',
                'object_task',
                'author_task',
                'employee_task',
                'line_task',
                'status_task',
            ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = \
            [
                'id',
                'name'
            ]


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = \
            [
                'id',
                'name',
                'department_id'
            ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = \
            [
                'id',
                'user',
                'chat_id',
                'position_dep_id_id'
            ]


class WorkTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTask
        fields = \
            [
                'id',
                'date_work_task',
                'time_work_task',
                'employee_work_task',
                'address_work_task',
                'task',
                'status_work_task'
            ]
