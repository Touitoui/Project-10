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
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permission_set',
        related_query_name='user',
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'password']


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='contributors')
    date_joined = models.DateTimeField(auto_now_add=True)
    # TODO: rename to date_created
    class Meta:
        unique_together = ('user', 'project')
        
    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
