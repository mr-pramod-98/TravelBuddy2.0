# Generated by Django 2.2.6 on 2019-11-03 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0017_auto_20191102_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleandgeneraldetails',
            name='reporting_time',
            field=models.TimeField(editable=False),
        ),
    ]