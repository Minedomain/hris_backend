# Generated by Django 3.1.8 on 2021-06-25 06:03

from django.db import migrations, models
import hris.apps.employees.models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0013_auto_20210625_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedocuments',
            name='docu_file_url',
            field=models.ImageField(max_length=255, upload_to=hris.apps.employees.models.documents),
        ),
        migrations.AlterField(
            model_name='employeesignature',
            name='employee_signature',
            field=models.ImageField(max_length=255, upload_to=hris.apps.employees.models.signature),
        ),
    ]
