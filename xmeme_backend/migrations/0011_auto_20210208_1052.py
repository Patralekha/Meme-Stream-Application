# Generated by Django 3.1.6 on 2021-02-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmeme_backend', '0010_auto_20210207_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='creationDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meme',
            name='lastUpdate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
