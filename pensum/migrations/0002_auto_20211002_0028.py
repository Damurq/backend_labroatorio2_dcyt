# Generated by Django 3.2.7 on 2021-10-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pensum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensum',
            name='date_issue',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pensum',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]