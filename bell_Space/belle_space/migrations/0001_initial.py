# Generated by Django 5.1.1 on 2024-10-16 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='belle_space.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255, null=True)),
                ('available_start_time', models.DateTimeField()),
                ('available_end_time', models.DateTimeField()),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('ตรวจสอบ', 'ตรวจสอบ'), ('ยกเลิก', 'ยกเลิก'), ('จองสำเร็จ', 'จองสำเร็จ')], default='ตรวจสอบ', max_length=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='belle_space.categories')),
                ('service', models.ManyToManyField(blank=True, to='belle_space.service')),
                ('staff', models.ManyToManyField(to='belle_space.staff')),
            ],
        ),
        migrations.CreateModel(
            name='UsersDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frist_name', models.CharField(max_length=155, null=True)),
                ('last_name', models.CharField(max_length=155, null=True)),
                ('birth_date', models.DateField()),
                ('phone_number', models.CharField(max_length=10, null=True, unique=True)),
                ('gender', models.CharField(choices=[('ผู้ชาย', 'M'), ('ผู้หญิง', 'F'), ('LGBTQ+', 'Lgbtq'), ('อื่นๆ', 'O')], max_length=10)),
                ('image_profile', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
