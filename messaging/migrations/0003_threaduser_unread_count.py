# Generated by Django 5.0.4 on 2024-05-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_threaduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='threaduser',
            name='unread_count',
            field=models.IntegerField(default=0),
        ),
    ]
