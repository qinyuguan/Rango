# Generated by Django 2.1.5 on 2021-08-05 07:08

from django.db import migrations, models
import shortuuidfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_merge_20210805_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default=uuid.uuid1, editable=False, max_length=22),
        ),
    ]