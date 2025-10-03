from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User, Contributor
from users.serializers import UserSerializer, ContributorSerializer
from users.permissions import IsAdminAuthenticated


class AdminUserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']

    def get_queryset(self):
        return User.objects.all()


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


class AdminContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAdminAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'user', 'project', 'created_time']

    def get_queryset(self):
        return Contributor.objects.all()


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'user', 'project', 'created_time']

    def get_queryset(self):
        ''' Return the contributors where user is the current user '''
        return Contributor.objects.filter(user=self.request.user.id)
    
    def perform_create(self, serializer):
        ''' Automatically set the user to the current user when creating a contributor '''
        serializer.save(user=self.request.user)

