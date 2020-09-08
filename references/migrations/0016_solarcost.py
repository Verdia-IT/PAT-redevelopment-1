# Generated by Django 2.2.5 on 2020-03-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0015_auto_20200302_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_size', models.IntegerField(unique=True)),
                ('single_site_dollar_per_watt', models.DecimalField(decimal_places=3, max_digits=5)),
                ('single_site_verdia_fee', models.DecimalField(decimal_places=3, max_digits=5)),
                ('multiple_site_dollar_per_watt', models.DecimalField(decimal_places=3, max_digits=5)),
                ('multiple_site_verdia_fee', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
    ]