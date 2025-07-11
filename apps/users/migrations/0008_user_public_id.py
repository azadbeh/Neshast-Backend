# Generated by Django 5.1.7 on 2025-06-03 13:44

import uuid

from django.db import migrations, models


def populate_public_id(apps, schema_editor):
    User = apps.get_model("users", "User")
    for user in User.objects.all():
        user.public_id = uuid.uuid4()
        user.save(update_fields=["public_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_remove_user_profile_picture_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="public_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.RunPython(populate_public_id, reverse_code=migrations.RunPython.noop),
    ]
