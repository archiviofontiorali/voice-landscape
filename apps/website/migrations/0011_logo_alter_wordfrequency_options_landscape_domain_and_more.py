# Generated by Django 4.2.5 on 2023-09-06 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0010_leafletprovider_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Logo",
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
                ("name", models.CharField(blank=True, max_length=150)),
                (
                    "image",
                    models.ImageField(
                        height_field="height", upload_to="logos/", width_field="width"
                    ),
                ),
                (
                    "width",
                    models.PositiveSmallIntegerField(
                        blank=True, editable=False, null=True
                    ),
                ),
                (
                    "height",
                    models.PositiveSmallIntegerField(
                        blank=True, editable=False, null=True
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="wordfrequency",
            options={
                "ordering": ("-frequency",),
                "verbose_name_plural": "Word Frequencies",
            },
        ),
        migrations.AddField(
            model_name="landscape",
            name="domain",
            field=models.URLField(
                blank=True,
                help_text="The domain to show. Leave blank to use the default one set in .env",
            ),
        ),
        migrations.AddField(
            model_name="landscape",
            name="logo_event",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="website.logo",
            ),
        ),
        migrations.AddField(
            model_name="landscape",
            name="logo_organizer",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="website.logo",
            ),
        ),
        migrations.AddField(
            model_name="landscape",
            name="logo_partners",
            field=models.ManyToManyField(
                blank=True, related_name="+", to="website.logo"
            ),
        ),
    ]
