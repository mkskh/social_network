# Generated by Django 5.0.4 on 2024-05-15 09:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0003_rename_seller_product_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="user",
            new_name="seller",
        ),
    ]