# Generated by Django 4.2.5 on 2023-09-13 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0011_logo_alter_wordfrequency_options_landscape_domain_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="landscape",
            name="enabled",
            field=models.BooleanField(
                default=True,
                help_text="Set to False to hide it in views, unless is chosen as default",
            ),
        ),
        migrations.AlterField(
            model_name="landscape",
            name="domain",
            field=models.URLField(
                blank=True,
                help_text="Domain in showcase page. Leave blank to use the one in .env",
            ),
        ),
    ]