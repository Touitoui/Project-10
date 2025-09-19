from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
User = settings.AUTH_USER_MODEL

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=False, blank=False)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'password']


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='contributors')
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'project')
        
    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
