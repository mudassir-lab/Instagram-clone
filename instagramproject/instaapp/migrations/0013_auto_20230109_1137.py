# Generated by Django 2.2 on 2023-01-09 11:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0012_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='story',
            field=models.FileField(upload_to='Stories_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]
