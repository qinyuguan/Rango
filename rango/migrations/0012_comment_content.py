# Generated by Django 2.1.5 on 2021-08-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0011_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
