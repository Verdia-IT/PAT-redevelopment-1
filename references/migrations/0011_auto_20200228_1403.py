# Generated by Django 2.2.5 on 2020-02-28 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0010_auto_20200228_1401'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='existinglight',
            options={'ordering': ('name',)},
        ),
    ]
