# Generated by Django 3.2.6 on 2021-09-27 22:30

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_alter_courses_course_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='field',
            field=models.FileField(upload_to=main_app.models.upload_location_content),
        ),
    ]
