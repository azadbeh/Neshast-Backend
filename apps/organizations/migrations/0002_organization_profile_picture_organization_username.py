# Generated by Django 5.1.7 on 2025-04-15 21:48

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="organization_profile_pictures/"),
        ),
        migrations.AddField(
            model_name="organization",
            name="username",
            field=models.CharField(
                default=None,
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
            ),
            preserve_default=False,
        ),
    ]
