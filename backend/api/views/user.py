from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from backend.api.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import action
from backend.api.models import TaskRequest
from backend.api.views.request import RequestSerializer


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                  'phone', 'identity_number', 'identity_type', 'level', 'city', 'description')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    pending_read_only_fields = ('username', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                                'identity_number', 'identity_type', 'level', 'city')

    anonymous_hiding_fields = ('identity_number', 'identity_type')

    def __init__(self, anonymous=False, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
            self.fields.pop('password')  # remove password field because we can't modify it in this way
        if anonymous:
            self.anonymous_clean()

    def create(self, validated_data):
        # Use create_user to ensure password is hashed
        instance = UserProfile.objects.create_user(**validated_data)
        return instance

    def anonymous_clean(self):
        # Remove identity field for anonymous
        for f in self.anonymous_hiding_fields:
            self.fields.pop(f)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        curr_user = self.request.user  # Login user
        instance = self.get_object()  # Requested user
        serializer = self.get_serializer(instance)
        if curr_user != instance and not curr_user.is_superuser:
            serializer.anonymous_clean()
        return Response(serializer.data)
        pass

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            users = UserProfile.objects.all()
        else:
            users = UserProfile.objects.filter(username=user.username)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Admin only
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)

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
            else:
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Old password or new password cannot be empty."}, status=status.HTTP_403_FORBIDDEN)
        pass
