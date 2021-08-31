# Generated by Django 3.1.8 on 2021-06-22 08:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employee_employee_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='leave_count',
            new_name='sick_leave_count',
        ),
        migrations.AddField(
            model_name='employee',
            name='vac_leave_count',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(15)]),
        ),
    ]
