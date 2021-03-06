from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CurrentUserDefault
from backend.api.models import Task, TaskRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from backend.api.views.user import BasicUserSerializer


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'creator', 'type', 'name', 'description', 'request_population',
                  'recruited_population', 'end_time', 'photo', 'edit_time', 'status')
        read_only_fields = ('id', 'creator')

    pending_read_only_fields = ('type', 'name', 'edit_time', 'status')

    creator = BasicUserSerializer(default=CurrentUserDefault())
    recruited_population = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
                # self.fields.pop('parent') # or remove the field

    def get_recruited_population(self, obj):
        return TaskRequest.objects.filter(task=obj, status=1).count()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        task_creator = self.request.query_params.get('user', None)
        if task_creator:
            queryset = queryset.filter(creator=task_creator)
        task_name = self.request.query_params.get('name', None)
        if task_name:
            queryset = queryset.filter(name__icontains=task_name)
        task_type = self.request.query_params.get('type', None)
        if task_type:
            queryset = queryset.filter(type=task_type)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creator=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator == self.request.user or self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator == self.request.user:
            serializer = self.get_serializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator == self.request.user or self.request.user.is_superuser:
            count = TaskRequest.objects.filter(task=task, status=1).count()
            if count == 0:
                task.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': "Cannot delete task with accepted request."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=["POST"], detail=True)
    def cancel(self, request, pk=None):
        task = self.get_object()
        if task.creator == self.request.user or self.request.user.is_superuser:
            task.status = 2
            task.save()
            return Response()
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        pass
