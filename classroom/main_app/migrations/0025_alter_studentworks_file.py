# Generated by Django 3.2.6 on 2021-10-02 15:27

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_alter_classwork_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentworks',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=main_app.models.upload_location),
        ),
    ]
