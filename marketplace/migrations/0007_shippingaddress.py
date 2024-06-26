# Generated by Django 5.0.4 on 2024-05-24 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0006_product_condition"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shipping_full_name", models.CharField(max_length=225)),
                ("shipping_email", models.CharField(max_length=225)),
                ("shipping_address1", models.CharField(max_length=225)),
                ("shipping_address2", models.CharField(max_length=225)),
                ("city", models.CharField(max_length=225)),
                ("state", models.CharField(blank=True, max_length=225, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=225, null=True)),
                ("country", models.CharField(max_length=225)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Shipping Address",
            },
        ),
    ]
