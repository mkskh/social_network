# Generated by Django 5.0.4 on 2024-05-26 14:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_thread_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]