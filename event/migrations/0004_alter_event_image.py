# Generated by Django 5.0 on 2024-01-23 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event/upload'),
        ),
    ]
