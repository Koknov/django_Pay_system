# Generated by Django 3.1.8 on 2021-04-25 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('wallet_number', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('total', models.IntegerField(default=5000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.IntegerField()),
                ('receiver_wallet_number', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='receiver_wallet', to=settings.AUTH_USER_MODEL)),
                ('sender_wallet_number', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='senders_wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
