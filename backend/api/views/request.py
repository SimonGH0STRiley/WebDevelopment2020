from rest_framework.serializers import ModelSerializer
from backend.api.models import TaskRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

TASK_PENDING = 0
TASK_ACCEPT = 1
TASK_REJECT = 2
TASK_CANCELED = 3


class RequestSerializer(ModelSerializer):
    class Meta:
        model = TaskRequest
        fields = '__all__'
        read_only_fields = ('creator', 'status')

    pending_read_only_fields = ('task',)

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
                # self.fields.pop('parent') # or remove the field


class RequestViewSet(ModelViewSet):
    queryset = TaskRequest.objects.all()
    serializer_class = RequestSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = TaskRequest.objects
        request_type = self.request.query_params.get('type', None)
        if request_type == 'task':
            queryset = queryset.filter(task__creator=user)
        elif request_type == 'request':
            queryset = queryset.filter(creator=user)
        elif not user.is_superuser:
            queryset = []
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        if instance.creator == user or instance.task.creator == user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creator=request.user, status=TASK_PENDING)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        pass

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == TASK_PENDING and instance.creator == self.request.user:
            serializer: RequestSerializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "This request has been accepted, rejected or canceled."},
                            status=status.HTTP_403_FORBIDDEN)
        pass

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != TASK_ACCEPT and instance.creator == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        pass

    @action(methods=['POST'], detail=True)
    def response(self, request, pk=None):
        task_request = self.get_object()
        if task_request.status != TASK_PENDING:
            return Response({"error": "This request has been accepted, rejected or canceled."},
                            status=status.HTTP_403_FORBIDDEN)
        task = task_request.task
        if task.creator != self.request.user:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        request_type = self.request.query_params.get('type', None)
        if request_type == 'accept':
            exist_count = TaskRequest.objects.filter(task=task, status=TASK_ACCEPT).count()
            if exist_count >= task.request_population:
                return Response({"error": "Task has reached its maximum requests."}, status=status.HTTP_403_FORBIDDEN)
            task_request.status = TASK_ACCEPT
            task_request.save()
            if exist_count + 1 >= task.request_population:
                queryset = TaskRequest.objects.filter(task=task, status=TASK_PENDING)
                queryset.update(status=TASK_REJECT)
                queryset.save()
            return Response(RequestSerializer(task_request).data)
            pass
        elif request_type == 'reject':
            # Rejecting doesn't change other objects
            task_request.status = TASK_REJECT
            task_request.save()
            return Response(RequestSerializer(task_request).data)
            pass
        pass

    @action(methods=['POST'], detail=True)
    def cancel(self, request, pk=None):
        task_request = self.get_object()
        if task_request.creator != self.request.user:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        if task_request.status != TASK_PENDING:
            return Response({"error": "The request cannot be canceled."}, status=status.HTTP_403_FORBIDDEN)

        pass

    pass
