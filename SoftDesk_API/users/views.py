from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import date

from users.models import User, Contributor
from users.serializers import UserSerializer, ContributorSerializer
from users.permissions import IsAdminAuthenticated

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
