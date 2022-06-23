from api import serializers
from rest_framework import generics
from task.models import Task
from rest_framework.permissions import IsAuthenticated


# API Вернуть все значения
class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated, )


# API Вернуть значение по id
class TaskDetail(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)


# API Добавить данные
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


# API Изменить, удалить данные
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
