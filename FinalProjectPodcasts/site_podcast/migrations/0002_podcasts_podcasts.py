# Generated by Django 4.0.4 on 2022-05-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_podcast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcasts',
            name='podcasts',
            field=models.CharField(default='Some String', max_length=100),
        ),
    ]