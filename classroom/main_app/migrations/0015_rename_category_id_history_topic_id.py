# Generated by Django 3.2.6 on 2021-09-27 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_auto_20210927_1235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='category_id',
            new_name='topic_id',
        ),
    ]