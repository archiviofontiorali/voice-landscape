# Generated by Django 4.2.4 on 2023-08-17 11:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_alter_wordfrequency_place"),
    ]

    operations = [
        migrations.CreateModel(
            name="Landscape",
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
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("title", models.CharField(blank=True, max_length=100)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("places", models.ManyToManyField(blank=True, to="website.place")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
