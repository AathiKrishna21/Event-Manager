from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Myevents

@receiver(post_save, sender=User)
def create_myevents(sender, instance, created, **kwargs):
    if created:
        Myevents.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_myevents(sender, instance, **kwargs):
    instance.myevents.save()