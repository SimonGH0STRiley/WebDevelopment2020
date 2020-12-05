from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from backend.api.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                  'phone', 'identity_number', 'identity_type', 'level', 'city', 'description')
        extra_kwargs = {'password': {'write_only': True}}

    pending_read_only_fields = ('username', 'first_name', 'last_name', 'is_superuser', 'date_joined',
                                'identity_number', 'identity_type', 'level', 'city')

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # Lock fields if not creating user
            for f in self.pending_read_only_fields:
                self.fields.get(f).read_only = True
                # self.fields.pop('parent') # or remove the field

    def create(self, validated_data):
        # Use create_user to ensure password is hashed
        instance = UserProfile.objects.create_user(**validated_data)
        return instance


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

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
            serializer = self.serializer_class(data=request.data)
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
            serializer = self.serializer_class(instance, data=request.data, partial=True)
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
            pass
        else:
            return Response({"error": "Operation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
