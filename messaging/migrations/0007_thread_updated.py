# Generated by Django 5.0.4 on 2024-05-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_remove_thread_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
