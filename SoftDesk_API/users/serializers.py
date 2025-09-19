from rest_framework.serializers import ModelSerializer, ValidationError, StringRelatedField
from datetime import date

from users.models import User, Contributor
from project.serializers import ProjectSerializer
 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'date_of_birth', 'username', 'email', 'password', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if not value.isalnum():
            raise ValidationError("Username must be alphanumeric.")
        return value

    def validate_date_of_birth(self, value):
        print(f"User is {(date.today() - value).days} days old")
        if value is not None and (date.today() - value).days < 5475:  # 15 years in days
            raise ValidationError("User must be at least 15 years old.")
        return value


class ContributorSerializer(ModelSerializer):
    # user = StringRelatedField()    
    project_info = ProjectSerializer(read_only=True, source='project')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'project_info', 'created_time']
        extra_kwargs = {'user': {'read_only': True}}

