# Generated by Django 4.1.4 on 2022-12-13 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ups',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]