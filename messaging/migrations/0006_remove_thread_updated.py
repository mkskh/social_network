# Generated by Django 5.0.4 on 2024-05-26 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_thread_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='updated',
        ),
    ]
