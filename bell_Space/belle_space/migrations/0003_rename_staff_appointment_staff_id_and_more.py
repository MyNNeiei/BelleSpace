# Generated by Django 5.1.1 on 2024-10-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belle_space', '0002_remove_staff_position_remove_usersdetail_frist_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='staff',
            new_name='staff_id',
        ),
        migrations.AlterField(
            model_name='staff',
            name='available_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='available_start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
