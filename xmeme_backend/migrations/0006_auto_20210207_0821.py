# Generated by Django 3.1.6 on 2021-02-07 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmeme_backend', '0005_auto_20210205_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='updatedDateTime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='meme',
            name='creationDateTime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
