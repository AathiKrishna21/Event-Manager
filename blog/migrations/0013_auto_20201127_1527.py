# Generated by Django 3.1.1 on 2020-11-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_etime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='event',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
