# Generated by Django 3.1.8 on 2021-06-24 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_auto_20210624_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='dept_role',
            new_name='department_role',
        ),
    ]