from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
class Post(models.Model):
    event = models.CharField(max_length = 100,unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="thumbnail") 
    register_file = models.FileField(blank=True, upload_to='List')
    etime = models.DateTimeField()


    def delete(self):
        path=self.register_file.path
        if os.path.isfile(path):
            os.remove(path)
        super(Post, self).delete()

    def save(self):
        f_name= self.event
        f_name=f_name + ".csv"
        self.register_file.save(f_name, ContentFile("Name,Reg No,E-Mail,Phone No,Deptartment,Event"),save=False)
        super().save()
        img = Image.open(self.image.path)

        if img.height > 500 or img.width>500:
            size=(500,500)
            img.thumbnail(size)
            img.save(self.image.path)

    def __str__(self):
        return self.event

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

@receiver(post_delete, sender=Post)
def photo_post_delete_handler(sender, **kwargs):
    photo = kwargs['instance']
    if photo.image.path != os.path.join(BASE_DIR, 'media\default.jpg'):
        storage, path = photo.image.storage, photo.image.path
        storage.delete(path)

