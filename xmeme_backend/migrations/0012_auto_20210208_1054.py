# Generated by Django 3.1.6 on 2021-02-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmeme_backend', '0011_auto_20210208_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='lastUpdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
