# Generated by Django 4.1 on 2022-12-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0005_standort_restaurant_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="standort_restaurant",
            name="phone",
            field=models.TextField(default="default value", max_length=200),
        ),
    ]
