from rest_framework.serializers import ModelSerializer, CurrentUserDefault, PrimaryKeyRelatedField
from backend.api.models import TaskRequest, FinishTaskDetail, IncomeSummary
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from backend.api.views.task import TaskSerializer
from backend.api.views.user import BasicUserSerializer

REQUEST_PENDING = 0
REQUEST_ACCEPT = 1
REQUEST_REJECT = 2
REQUEST_CANCELED = 3


class RequestSerializer(ModelSerializer):
    class Meta:
        model = TaskRequest
        fields = '__all__'
        read_only_fields = ('creator', 'status', 'create_time', 'edit_time')

    pending_read_only_fields = ('task',)
    creator = BasicUserSerializer(default=CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
                # self.fields.pop('parent') # or remove the field

    def to_representation(self, instance):
        # Show the whole task instead of an id
        ret = super().to_representation(instance)
        ret['task'] = TaskSerializer(instance.task).data
        return ret


def create_income_record(task, creator, executor, creator_expense, executor_expense=1):
    detail = FinishTaskDetail(task=task, creator=creator, executor=executor,
                              creator_expense=creator_expense, executor_expense=executor_expense)
    detail.save()
    today = detail.finish_time.date()
    summary, _ = IncomeSummary.objects.get_or_create(date=today, city=creator.city, task_type=task.type, defaults={
         'finish_number': 0, 'income': 0
    })
    summary.finish_number += 1
    summary.income += (creator_expense + executor_expense)
    summary.save()
    pass


class RequestViewSet(ModelViewSet):
    queryset = TaskRequest.objects.all()
    serializer_class = RequestSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = TaskRequest.objects
        request_creator = self.request.query_params.get('creator', None)
        request_name = self.request.query_params.get('name', None)
        request_sort = self.request.query_params.get('sort', None)
        if request_creator == 'task':
            queryset = queryset.filter(task__creator=user)
        elif request_creator == 'request':
            queryset = queryset.filter(creator=user)
        elif not user.is_superuser:
            queryset = queryset.none()
        if request_name:
            queryset = queryset.filter(task__name__icontains=request_name)
        if request_sort:
            pass
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
            serializer.save(creator=request.user, status=REQUEST_PENDING)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        pass

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == REQUEST_PENDING and instance.creator == self.request.user:
            serializer: RequestSerializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "This request has been accepted, rejected or canceled."},
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != REQUEST_ACCEPT and instance.creator == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], detail=True)
    def response(self, request, pk=None):
        task_request = self.get_object()
        if task_request.status != REQUEST_PENDING:
            return Response({"error": "This request has been accepted, rejected or canceled."},
                            status=status.HTTP_403_FORBIDDEN)
        task = task_request.task
        if task.creator != self.request.user:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        request_type = self.request.POST.get('type', None)
        if request_type == 'accept':
            exist_count = TaskRequest.objects.filter(task=task, status=REQUEST_ACCEPT).count()
            if exist_count >= task.request_population:
                return Response({"error": "Task has reached its maximum requests."}, status=status.HTTP_403_FORBIDDEN)
            task_request.status = REQUEST_ACCEPT
            task_request.save()
            # insert a record to income tables
            create_income_record(task, task.creator, task_request.creator, 3, 1)
            if exist_count + 1 >= task.request_population:
                queryset = TaskRequest.objects.filter(task=task, status=REQUEST_PENDING)
                queryset.update(status=REQUEST_REJECT)
                task.status = 1  # Finished
            return Response(RequestSerializer(task_request).data)
        elif request_type == 'reject':
            # Rejecting doesn't change other objects
            task_request.status = REQUEST_REJECT
            task_request.save()
            return Response(RequestSerializer(task_request).data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)


    @action(methods=['POST'], detail=True)
    def cancel(self, request, pk=None):
        task_request = self.get_object()
        if task_request.creator != self.request.user:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        if task_request.status != REQUEST_PENDING:
            return Response({"error": "The request cannot be canceled."}, status=status.HTTP_403_FORBIDDEN)
        task_request.status = REQUEST_CANCELED
        task_request.save()
        return Response(RequestSerializer(task_request).data)
    pass
