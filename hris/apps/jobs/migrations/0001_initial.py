# Generated by Django 3.1.8 on 2021-06-01 10:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('job_title', models.CharField(max_length=255)),
                ('duties', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('min_salary', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('max_salary', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True)),
            ],
        ),
    ]