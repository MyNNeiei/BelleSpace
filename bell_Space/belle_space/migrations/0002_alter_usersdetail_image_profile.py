# Generated by Django 5.1.1 on 2024-10-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belle_space', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdetail',
            name='image_profile',
            field=models.ImageField(null=True, upload_to='profile_pic'),
        ),
    ]
