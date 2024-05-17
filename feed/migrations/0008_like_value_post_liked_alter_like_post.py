# Generated by Django 5.0.4 on 2024-04-30 12:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_alter_comment_post_alter_like_post'),
        ('user', '0004_alter_userprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='value',
            field=models.CharField(blank=True, choices=[('Like', 'Like'), ('Unlike', 'Unlike')], max_length=8),
        ),
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='likes', to='user.userprofile'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.post'),
        ),
    ]