# Generated by Django 2.1 on 2020-04-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blink', '0005_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='icon',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]