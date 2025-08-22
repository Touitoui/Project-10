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

    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'password']
