# Generated by Django 2.2.6 on 2019-10-26 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0005_auto_20191026_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationdetails',
            name='visiting_on',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
