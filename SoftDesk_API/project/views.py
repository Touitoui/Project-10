from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from project.models import Project, Issue, Comment
from users.models import Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from users.permissions import IsAdminAuthenticated

class AdminProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.all()

        user_id = self.request.GET.get('id')
        if user_id is not None:
            queryset = queryset.filter(id=user_id)

        type_ = self.request.GET.get('type')
        if type_ is not None:
            queryset = queryset.filter(type=type_)

        author = self.request.GET.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)

        return queryset

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()
    
    def get_your_projects(self):
        user = self.request.user
        return Project.objects.filter(author=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(f"Creating project with data: {serializer.validated_data}")
        project = Project.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description', ''),
            type=serializer.validated_data['type'],
            author=request.user
        )
        Contributor.objects.create(user=request.user, project=project)
        return Response(ProjectSerializer(project).data, status=201)

class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

