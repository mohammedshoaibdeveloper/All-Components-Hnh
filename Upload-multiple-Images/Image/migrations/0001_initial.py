# Generated by Django 3.0.1 on 2020-08-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadPdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumes', models.FileField(blank=True, null=True, upload_to='resumes/')),
            ],
        ),
    ]
