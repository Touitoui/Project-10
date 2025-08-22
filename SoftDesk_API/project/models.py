from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Project(models.Model):
    TYPE_CHOICES = (
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'), 
        ('IOS', 'iOS'),
        ('ANDROID', 'Android')
    )
    
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='authored_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Issue(models.Model):
    STATUS_CHOICES = (
        ('TODO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('FINISHED', 'Terminé')
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Élevée')
    )
    TAG_CHOICES = (
        ('BUG', 'Bug'),
        ('TASK', 'Tâche'),
        ('ENHANCEMENT', 'Amélioration')
    )
    
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='MEDIUM')
    tag = models.CharField(max_length=11, choices=TAG_CHOICES, default='TASK')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    created_time = models.DateTimeField(auto_now_add=True)