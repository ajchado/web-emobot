# Generated by Django 3.2.9 on 2021-11-16 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('gender', models.CharField(max_length=20)),
                ('shortbio', models.CharField(max_length=100)),
                ('isLoggedIn', models.BooleanField(default=False)),
                ('isAdmin', models.BooleanField(default=True)),
                ('profilePicture', models.FileField(default='settings.MEDIA_ROOT/default.jpg', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('personID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('gender', models.CharField(max_length=20)),
                ('shortbio', models.CharField(max_length=100)),
                ('isLoggedIn', models.BooleanField(default=False)),
                ('isDeleted', models.IntegerField(default=0)),
                ('isAdmin', models.BooleanField(default=False)),
                ('profilePicture', models.FileField(default='settings.MEDIA_ROOT/default.jpg', upload_to='')),
            ],
        ),
    ]