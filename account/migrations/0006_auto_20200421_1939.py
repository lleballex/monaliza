# Generated by Django 2.2.6 on 2020-04-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200416_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_birth',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='age'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=30, null=True, verbose_name='gender'),
        ),
    ]
