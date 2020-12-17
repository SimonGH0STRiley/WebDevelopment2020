from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from backend.api.models import IncomeSummary
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class StatSerializer(ModelSerializer):
    class Meta:
        model = IncomeSummary
        fields = '__all__'


class StatView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               GenericViewSet):
    queryset = IncomeSummary.objects.all()
    serializer_class = StatSerializer
    permission_classes = [IsAdmin]

    pass
