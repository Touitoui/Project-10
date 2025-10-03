from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from project.models import Project, Issue, Comment
from users.models import Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from users.permissions import IsAdminAuthenticated, IsAuthor, IsContributor


class AdminProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type', 'author', 'created_time']

    def get_queryset(self):
        return Project.objects.all()


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type', 'author', 'created_time']

    def get_queryset(self):
        return Project.objects.all()
    
    def perform_create(self, serializer):
        ''' Automatically set the author to the current user when creating a project '''
        serializer.save(author=self.request.user)


class AdminIssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAdminAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'status', 'priority', 'tag', 'project', 'author', 'created_time']

    def get_queryset(self):
        return Issue.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'status', 'priority', 'tag', 'project', 'author', 'created_time']

    def get_queryset(self):
        ''' Return issues for projects where the user is a contributor '''
        user_projects = Contributor.objects.filter(user=self.request.user).values_list('project', flat=True)
        return Issue.objects.filter(project__in=user_projects)

    def perform_create(self, serializer):
        ''' Automatically set the author to the current user when creating an issue '''
        serializer.save(author=self.request.user)


class AdminCommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAdminAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'issue', 'author', 'created_time']

    def get_queryset(self):
        return Comment.objects.all()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'issue', 'author', 'created_time']

    def get_queryset(self):
        ''' Return comments for issues in projects where the user is a contributor '''
        user_projects = Contributor.objects.filter(user=self.request.user).values_list('project', flat=True)
        return Comment.objects.filter(issue__project__in=user_projects)

    def perform_create(self, serializer):
        ''' Automatically set the author to the current user when creating a comment.'''
        serializer.save(author=self.request.user)
