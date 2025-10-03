from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Project
from users.models import Contributor


@receiver(post_save, sender=Project)
def create_contributor(sender, instance, created=False, **kwargs): 
    project = instance
    # Only create contributor for new projects and after the project is saved
    if not Contributor.objects.filter(user=project.author, project=project).exists():
        Contributor.objects.create(user=project.author, project=project)