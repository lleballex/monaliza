# Generated by Django 3.0.5 on 2020-05-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tag_1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag_2',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag_3',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag_4',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag_5',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
