from rest_framework.serializers import ModelSerializer, ValidationError
from datetime import date
from project.models import Project, Issue, Comment
 
class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}

    def validate_name(self, value):
        print(f"Validating name: {value}")
        if not value.isalnum():
            raise ValidationError("Name must be alphanumeric.")
        return value

    # def validate_type(self, value):
    #     print(f"Validating type: {value} - {value not in dict(Project.TYPE_CHOICES).keys()}")
    #     if value not in dict(Project.TYPE_CHOICES).keys():
    #         raise ValidationError("Type must be one of: " + ", ".join(dict(Project.TYPE_CHOICES).keys()))
    #     return value

    # def validate_description(self, value):
    #     if not value:
    #         raise ValidationError("Description is required.")
    #     return value


class IssueSerializer(ModelSerializer):
 
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'project']

    def validate_title(self, value):
        if not value:
            raise ValidationError("Title is required.")
        return value

    def validate_description(self, value):
        if not value:
            raise ValidationError("Description is required.")
        return value


class CommentSerializer(ModelSerializer):
 
    class Meta:
        model = Comment
        fields = ['id', 'content', 'issue', 'user']

    def validate_content(self, value):
        if not value:
            raise ValidationError("Content is required.")
        return value
