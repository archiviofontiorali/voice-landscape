# Generated by Django 4.2.4 on 2023-08-18 19:33

import apps.website.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_landscape_provider"),
    ]

    operations = [
        migrations.AddField(
            model_name="landscape",
            name="default",
            field=apps.website.fields.UniqueBooleanField(default=False),
        ),
    ]
