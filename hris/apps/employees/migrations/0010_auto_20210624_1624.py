# Generated by Django 3.1.8 on 2021-06-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20210623_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department_role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('HR', 'HR'), ('Normal', 'Normal')], default='Normal', max_length=255),
        ),
    ]
