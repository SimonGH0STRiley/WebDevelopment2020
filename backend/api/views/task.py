from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, CurrentUserDefault, StringRelatedField
from backend.api.models import Task
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth import get_user_model


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'creator', 'type', 'name', 'description', 'request_population',
                  'recruited_population', 'end_time', 'photo', 'edit_time', 'status')
        read_only_fields = ('id',)

    pending_read_only_fields = ('creator', 'type', 'name', 'recruited_population', 'status')
    creator = StringRelatedField(read_only=True)

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
                # self.fields.pop('parent') # or remove the field


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        task_name = self.request.query_params.get('name', None)
        if task_name:
            queryset = queryset.filter(name__icontains=task_name)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer: ModelSerializer = self.get_serializer(data=request.data)
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
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator == self.request.user or self.request.user.is_superuser:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
