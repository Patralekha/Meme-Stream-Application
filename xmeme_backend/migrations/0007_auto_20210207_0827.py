# Generated by Django 3.1.6 on 2021-02-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmeme_backend', '0006_auto_20210207_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meme',
            name='creationDateTime',
        ),
        migrations.AddField(
            model_name='meme',
            name='creationDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
