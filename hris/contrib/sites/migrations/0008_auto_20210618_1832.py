# Generated by Django 3.1.8 on 2021-06-18 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0007_auto_20210614_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['domain'], 'verbose_name': 'site', 'verbose_name_plural': 'sites'},
        ),
    ]