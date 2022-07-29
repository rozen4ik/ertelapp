from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import TaskSerializer, WorkTaskSerializer
from task.models import Task
from work_task.models import WorkTask


@api_view(['GET', 'POST'])
def api_task_list(request, employee_task):
    if request.method == 'GET':
        user = User.objects.get(username=employee_task)
        tasks = Task.objects.filter(employee_task=f"{user.first_name} {user.last_name}").order_by("-id")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_task_detail(request, pk, employee_task):
    try:
        user = User.objects.get(username=employee_task)
        task = Task.objects.get(pk=pk, employee_task=f"{user.first_name} {user.last_name}")
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def api_work_task_list(request):
    if request.method == 'GET':
        work_tasks = WorkTask.objects.all().order_by("-id")
        serializer = WorkTaskSerializer(work_tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_work_task_detail(request, pk):
    try:
        work_task = WorkTask.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WorkTaskSerializer(work_task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WorkTaskSerializer(work_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        work_task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
