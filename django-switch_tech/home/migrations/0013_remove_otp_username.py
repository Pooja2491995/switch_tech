# Generated by Django 4.1.7 on 2023-02-28 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_otp_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='username',
        ),
    ]