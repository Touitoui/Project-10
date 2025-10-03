from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Project
from users.models import Contributor


@receiver(post_save, sender=Project)
def create_contributor(sender, instance, created=False, **kwargs): 
    print(f"Signal received for project: {project}")
    # Only create contributor for new projects and after the project is saved
    if not Contributor.objects.filter(user=project.author, project=project).exists():
        print(f"Creating contributor for user: {project.author} in project: {project.name}")
        Contributor.objects.create(user=project.author, project=project)