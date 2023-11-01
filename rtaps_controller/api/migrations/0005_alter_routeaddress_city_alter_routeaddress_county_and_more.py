# Generated by Django 4.2.6 on 2023-10-30 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_accidentprobability_routeaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routeaddress',
            name='city',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='routeaddress',
            name='county',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='routeaddress',
            name='establishment',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='routeaddress',
            name='route',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
