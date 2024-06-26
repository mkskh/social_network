# Generated by Django 5.0.4 on 2024-05-24 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0007_shippingaddress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shippingaddress",
            name="city",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="country",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="shipping_address1",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="shipping_address2",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="shipping_email",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="shipping_full_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="zipcode",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
