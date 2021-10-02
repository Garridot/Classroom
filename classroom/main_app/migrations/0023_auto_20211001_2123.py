# Generated by Django 3.2.6 on 2021-10-02 00:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_alter_teachers_courses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classwork',
            old_name='due_date',
            new_name='deadline',
        ),
        migrations.RemoveField(
            model_name='classwork',
            name='reply',
        ),
        migrations.CreateModel(
            name='StudentWorks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=main_app.models.upload_location_assignment)),
                ('comment', models.TextField(blank=True, null=True)),
                ('grade', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(choices=[('Passed', 'Passed'), ('Unchecked', 'Unchecked'), ('Failed', 'Failed')], default='male', max_length=10)),
                ('asignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.teachers')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.courses')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.students')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.coursetopic')),
            ],
        ),
    ]