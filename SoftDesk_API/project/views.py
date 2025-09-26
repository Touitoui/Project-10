from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from project.models import Project, Issue, Comment
from users.models import Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from users.permissions import IsAdminAuthenticated, IsAuthor, IsContributor

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

        created_time = self.request.GET.get('created_time')
        if created_time is not None:
            queryset = queryset.filter(created_time=created_time)

        return queryset
    

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

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

        created_time = self.request.GET.get('created_time')
        if created_time is not None:
            queryset = queryset.filter(created_time=created_time)

        return queryset
    
    def perform_create(self, serializer):
        ''' Automatically set the author to the current user when creating a project '''
        serializer.save(author=self.request.user)

class AdminIssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()

        issue_id = self.request.GET.get('id')
        if issue_id is not None:
            queryset = queryset.filter(id=issue_id)

        title = self.request.GET.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)

        status = self.request.GET.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        priority = self.request.GET.get('priority')
        if priority is not None:
            queryset = queryset.filter(priority=priority)

        tag = self.request.GET.get('tag')
        if tag is not None:
            queryset = queryset.filter(tag=tag)

        project = self.request.GET.get('project')
        if project is not None:
            queryset = queryset.filter(project=project)

        author = self.request.GET.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)

        created_time = self.request.GET.get('created_time')
        if created_time is not None:
            queryset = queryset.filter(created_time=created_time)

        return queryset

class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

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

    def get_queryset(self):
        queryset = Comment.objects.all()

        comment_id = self.request.GET.get('id')
        if comment_id is not None:
            queryset = queryset.filter(id=comment_id)

        issue_id = self.request.GET.get('issue')
        if issue_id is not None:
            queryset = queryset.filter(issue=issue_id)

        author = self.request.GET.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)

        created_time = self.request.GET.get('created_time')
        if created_time is not None:
            queryset = queryset.filter(created_time=created_time)

        return queryset


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        ''' Return comments for issues in projects where the user is a contributor '''
        user_projects = Contributor.objects.filter(user=self.request.user).values_list('project', flat=True)
        return Comment.objects.filter(issue__project__in=user_projects)

    def perform_create(self, serializer):
        ''' Automatically set the author to the current user when creating a comment.'''
        serializer.save(author=self.request.user)
