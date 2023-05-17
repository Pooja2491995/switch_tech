# Generated by Django 4.1.7 on 2023-03-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_coursesuggession_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesuggession',
            name='difficulty',
            field=models.CharField(choices=[('BG', 'Begginer'), ('IN', 'Intermediat'), ('AD', 'Advanced')], default='BG', max_length=2),
        ),
    ]