# Generated by Django 2.1 on 2020-04-21 17:13

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blink', '0004_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(blank=True, default='https://userpic.codeforces.com/no-avatar.jpg', null=True, upload_to='profilePhoto/%Y/%m/%D/')),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('country', django_countries.fields.CountryField(blank=True, default='', max_length=2, null=True)),
                ('type', models.TextField(blank=True, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')], null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('qualifications', models.TextField(default='Qualifications are adjustable')),
                ('description', models.TextField()),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('vacancy', models.IntegerField(blank=True, null=True)),
                ('salary_min', models.IntegerField(blank=True, null=True)),
                ('salary_max', models.IntegerField(blank=True, null=True)),
                ('benefits', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blink.User')),
            ],
        ),
    ]