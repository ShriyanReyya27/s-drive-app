# Generated by Django 4.2.6 on 2023-10-25 01:22

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=50, unique=True)),
                ('id', models.CharField(default=api.models.generate_id, max_length=20, primary_key=True, serialize=False)),
            ],
        ),
    ]
