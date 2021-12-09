# Generated by Django 3.2.6 on 2021-10-04 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main_app', '0035_auto_20211004_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='receiver',
        ),
        migrations.AddField(
            model_name='notifications',
            name='receivers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to='auth.group'),
        ),
    ]