# Generated by Django 5.0.4 on 2024-04-23 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_post_comments_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
