# Generated by Django 4.1.7 on 2023-03-06 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_coursesuggession_course_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesuggession',
            name='difficulty',
            field=models.CharField(choices=[('BG', 'Begginer'), ('IN', 'Intermediate'), ('AD', 'Advanced')], default='BG', max_length=2),
        ),
    ]
