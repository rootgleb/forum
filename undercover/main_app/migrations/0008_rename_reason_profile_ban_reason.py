# Generated by Django 4.1.5 on 2023-04-23 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_profile_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='reason',
            new_name='ban_reason',
        ),
    ]
