# Generated by Django 5.0.6 on 2024-05-29 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplyPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.CharField(max_length=12, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('serial_number', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('reading_type', models.CharField(blank=True, choices=[], max_length=2, null=True)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='carrots.manufacturer')),
                ('supply_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='carrots.supplypoint')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=4, max_digits=16)),
                ('read_at', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('reading_method', models.CharField(blank=True, choices=[('N', 'Not viewed by an Agent'), ('P', 'Viewed by an Agent'), ('S', 'Automatically collected via network'), ('T', 'Time based Reading')], max_length=4, null=True)),
                ('time_code', models.CharField(blank=True, max_length=2, null=True)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='carrots.meter')),
                ('supply_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='carrots.supplypoint')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
