# Generated by Django 4.1 on 2022-10-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0002_standort_restaurant_delete_standort"),
    ]

    operations = [
        migrations.AddField(
            model_name="standort_restaurant",
            name="city",
            field=models.CharField(default="default value", max_length=200),
        ),
        migrations.AddField(
            model_name="standort_restaurant",
            name="country",
            field=models.CharField(default="default value", max_length=200),
        ),
    ]
