# Generated by Django 3.1.8 on 2021-06-01 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('message_details', models.CharField(max_length=255)),
                ('message_date_sent', models.DateTimeField(auto_now_add=True)),
                ('message_is_read', models.BooleanField(default=False)),
                ('message_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_employee', to=settings.AUTH_USER_MODEL)),
                ('message_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('memo_subject', models.CharField(max_length=255)),
                ('memo_content', models.CharField(max_length=255)),
                ('memo_image', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('memo_date_created', models.DateTimeField(auto_now_add=True)),
                ('memo_posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memo_sender_employee', to=settings.AUTH_USER_MODEL)),
                ('memo_receiver_dept', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.department')),
                ('memo_receiver_employee', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memo_receiver_employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announce_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('announce_subject', models.CharField(max_length=255)),
                ('announce_content', models.CharField(max_length=255)),
                ('announce_date', models.DateTimeField(auto_now_add=True)),
                ('announce_posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]