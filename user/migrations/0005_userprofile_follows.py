# Generated by Django 5.0.4 on 2024-04-24 08:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_userprofile_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="follows",
            field=models.ManyToManyField(
                blank=True, related_name="followed_by", to="user.userprofile"
            ),
        ),
    ]