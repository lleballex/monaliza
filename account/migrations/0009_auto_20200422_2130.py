# Generated by Django 2.2.6 on 2020-04-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200422_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='account/avatars/%y/%m/%d'),
        ),
    ]
