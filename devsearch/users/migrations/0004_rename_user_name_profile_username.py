# Generated by Django 4.1.4 on 2023-01-04 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_profile_location_skill"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="user_name", new_name="username",
        ),
    ]
