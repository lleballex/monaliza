# Generated by Django 3.0.5 on 2020-05-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20200427_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
