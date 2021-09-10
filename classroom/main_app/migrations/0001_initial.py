# Generated by Django 3.2.6 on 2021-09-10 18:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('course_picture', models.ImageField(blank=True, null=True, upload_to='course_pictures')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='SchoolYears',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.CharField(max_length=8, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(choices=[('male', 'male'), ('feminine', 'feminine'), ('undefined', 'undefined')], default='male', max_length=10)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='teachers/profile_pictures')),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.CharField(max_length=8, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(choices=[('male', 'male'), ('feminine', 'feminine'), ('undefined', 'undefined')], default='male', max_length=10)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='students/profile_pictures')),
                ('HS_diploma', models.FileField(blank=True, null=True, upload_to='students/high_school_diploma')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schoolyears')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=100)),
                ('link', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('unread', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schoolyears')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('event_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.courses')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schoolyears')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.AddField(
            model_name='courses',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schoolyears'),
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.courses')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schoolyears')),
            ],
            options={
                'verbose_name': 'Course Content',
                'verbose_name_plural': 'Courses Content',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('field', models.FileField(upload_to='pdf')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.coursecategory')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menssage', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main_app.events')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('document', models.CharField(max_length=8)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('feminine', 'feminine'), ('undefined', 'undefined')], default='male', max_length=10)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='applications/profile_pictures')),
                ('HS_diploma', models.FileField(blank=True, null=True, upload_to='applications/high_school_diploma')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.schoolyears')),
            ],
        ),
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.CharField(max_length=8, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(choices=[('male', 'male'), ('feminine', 'feminine'), ('undefined', 'undefined')], default='male', max_length=10)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='admins/profile_pictures')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
            },
        ),
    ]
