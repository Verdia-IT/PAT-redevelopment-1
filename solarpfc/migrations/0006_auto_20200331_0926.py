# Generated by Django 2.2.5 on 2020-03-30 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solarpfc', '0005_auto_20200331_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarprice',
            name='solar_unit_cost_override',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True),
        ),
    ]
