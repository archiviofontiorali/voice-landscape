# Generated by Django 4.2.4 on 2023-08-28 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_share_landscape"),
    ]

    operations = [
        migrations.AlterField(
            model_name="share",
            name="landscape",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="website.landscape"
            ),
        ),
    ]
