# Generated by Django 2.1.5 on 2021-08-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_comment_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookdetail',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='category',
            name='views',
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='categories',
            field=models.ManyToManyField(to='rango.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=4096, unique=True),
        ),
    ]