from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField( upload_to="thumbnail") 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        
        if img.height > 500 or img.width>500:
            size=(500,500)
            img.thumbnail(size)
            img.save(self.image.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

@receiver(post_delete, sender=Post)
def photo_post_delete_handler(sender, **kwargs):
    photo = kwargs['instance']
    if photo.image:
        storage, path = photo.image.storage, photo.image.path
        storage.delete(path)