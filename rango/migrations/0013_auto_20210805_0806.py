# Generated by Django 2.1.5 on 2021-08-05 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_comment_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='category',
            name='views',
        ),
    ]
