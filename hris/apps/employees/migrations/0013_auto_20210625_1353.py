# Generated by Django 3.1.8 on 2021-06-25 05:53

from django.db import migrations, models
import hris.apps.employees.models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0012_auto_20210624_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignature',
            name='employee_signature',
            field=models.ImageField(blank=True, default=None, max_length=255, null=True, upload_to=hris.apps.employees.models.signature),
        ),
    ]
