# Generated by Django 3.2.6 on 2021-10-02 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_auto_20211001_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classwork',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
