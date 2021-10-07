# Generated by Django 3.2.7 on 2021-10-07 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pensum', '0002_auto_20211002_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('code', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.CharField(max_length=1000, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Commission',
            },
        ),
    ]