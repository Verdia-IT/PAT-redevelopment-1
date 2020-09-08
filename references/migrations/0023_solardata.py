# Generated by Django 2.2.5 on 2020-03-31 03:44

from django.db import migrations, models
import references.models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0022_lightingdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('solar_data_file', models.FileField(upload_to=references.models.solar_data_file_name)),
            ],
        ),
    ]