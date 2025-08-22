from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import date

from users.models import User, Contributor
from users.serializers import UserSerializer, ContributorSerializer
from users.permissions import IsAdminAuthenticated


class AdminUserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()

        user_id = self.request.GET.get('id')
        if user_id is not None:
            queryset = queryset.filter(id=user_id)

        can_be_contacted = self.request.GET.get('can_be_contacted')
        if can_be_contacted is not None:
            queryset = queryset.filter(can_be_contacted=can_be_contacted)

        can_data_be_shared = self.request.GET.get('can_data_be_shared')
        if can_data_be_shared is not None:
            queryset = queryset.filter(can_data_be_shared=can_data_be_shared)

        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create user with hashed password
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password'],
            date_of_birth=serializer.validated_data.get('date_of_birth')
        )
        return Response(UserSerializer(user).data, status=201)
    
    def patch(self, request, *args, **kwargs):
        if not request.data.get("id"):
            return Response({"error": "ID is required"}, status=400)
        user = User.objects.filter(id=request.data.get("id"))
        print(f"Updating user: {user}")
        serializer = self.get_serializer(user.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not request.data.get("id"):
            return Response({"error": "ID is required"}, status=400)
        user = User.objects.filter(id=request.data.get("id"))
        user.delete()
        return Response(status=204)

class RegisterUserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create user with hashed password
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password'],
            date_of_birth=serializer.validated_data.get('date_of_birth')
        )
        return Response(UserSerializer(user).data, status=201)
    

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        user = self.get_queryset()

        serializer = self.get_serializer(user.first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.get_queryset()
        user.delete()
        return Response(status=204)
