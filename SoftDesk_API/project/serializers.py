from rest_framework.serializers import ModelSerializer, ValidationError
from project.models import Project, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}

    def validate_name(self, value):
        print(f"Validating name: {value}")
        if not value.isalnum():
            raise ValidationError("Name must be alphanumeric.")
        return value


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'project', 'priority', 'tag', 'author', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}

