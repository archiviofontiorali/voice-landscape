# Generated by Django 4.2.4 on 2023-08-22 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_word_alter_wordfrequency_word"),
    ]

    operations = [
        migrations.AddField(
            model_name="share",
            name="landscape",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="website.landscape",
            ),
        ),
    ]
