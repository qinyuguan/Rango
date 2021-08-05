# Generated by Django 2.1.5 on 2021-08-04 19:59

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0006_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=255)),
                ('total_price', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('order_no', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('book', models.ManyToManyField(to='rango.BookDetail')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]