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


class RegisterUserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user with hashed password
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            date_of_birth=serializer.validated_data.get('date_of_birth'),
            can_data_be_shared=serializer.validated_data.get('can_data_be_shared', False),
            can_be_contacted=serializer.validated_data.get('can_be_contacted', False),
        )
        return Response(UserSerializer(user).data, status=201)


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Return the user instance for the current authenticated user '''
        return User.objects.filter(id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        user_instance = self.get_queryset().first()

        # Hash password if provided
        data = request.data.copy()
        if 'password' in data:
            user_instance.set_password(data['password'])
            user_instance.save()
            data.pop('password')

        serializer = self.get_serializer(user_instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AdminContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Return the contributors where user is the current user '''
        return Contributor.objects.filter(user=self.request.user.id)
    
    def perform_create(self, serializer):
        ''' Automatically set the user to the current user when creating a contributor '''
        serializer.save(user=self.request.user)

