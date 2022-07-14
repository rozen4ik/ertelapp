from api import serializers
from rest_framework import generics
from task.models import Task, WorkTask
from rest_framework.permissions import IsAuthenticated


# API Вернуть все значения
class TaskList(generics.ListAPIView):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated, )


# API Вернуть значение по id
class TaskDetail(generics.RetrieveAPIView):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated, )


# API Добавить данные
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()


# API Изменить, удалить данные
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)


class WorkTaskList(generics.ListAPIView):
    queryset = WorkTask.objects.all().order_by("-id")
    serializer_class = serializers.WorkTaskSerializer
    permission_classes = (IsAuthenticated, )


class WorkTaskDetail(generics.RetrieveAPIView):
    queryset = WorkTask.objects.all().order_by("-id")
    serializer_class = serializers.WorkTaskSerializer
    permission_classes = (IsAuthenticated, )


class WorkTaskList(generics.ListCreateAPIView):
    queryset = WorkTask.objects.all().order_by("-id")
    serializer_class = serializers.WorkTaskSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()


class WorkTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkTask.objects.all().order_by("-id")
    serializer_class = serializers.WorkTaskSerializer
    permission_classes = (IsAuthenticated, )
