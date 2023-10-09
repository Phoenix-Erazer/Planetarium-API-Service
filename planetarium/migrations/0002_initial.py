# Generated by Django 4.2.6 on 2023-10-09 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("planetarium", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="reservations",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="show_sessions",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="planetarium.showsession",
            ),
        ),
        migrations.AddField(
            model_name="showsession",
            name="astronomy_show",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="showsession",
            name="planetarium_dome",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="planetarium.astronomyshow",
            ),
        ),
        migrations.AddField(
            model_name="astronomyshow",
            name="description",
            field=models.ManyToManyField(
                related_name="astronomy_shows", to="planetarium.showtheme"
            ),
        ),
    ]
