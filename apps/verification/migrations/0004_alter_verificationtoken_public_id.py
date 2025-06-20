# Generated by Django 5.1.7 on 2025-06-03 14:01

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("verification", "0003_verificationtoken_public_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="verificationtoken",
            name="public_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
