from rest_framework.serializers import ModelSerializer, ValidationError, StringRelatedField, HiddenField
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
    project_info = ProjectSerializer(read_only=True, source='project')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'project', "project_info", "status", 'priority', "tag", 'author', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}


class CommentSerializer(ModelSerializer):
    issue_info = IssueSerializer(read_only=True, source='issue')
    # # user = StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'issue_info', 'author', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}

