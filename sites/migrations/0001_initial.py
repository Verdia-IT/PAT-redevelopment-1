# Generated by Django 2.2.5 on 2020-03-06 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0002_auto_20200306_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=50)),
                ('NMI', models.CharField(max_length=13)),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('New South Wales', 'New South Wales'), ('Northern Territory', 'Northern Territory'), ('Queensland', 'Queensland'), ('Victoria', 'Victoria'), ('South Australia', 'South Australia'), ('Australian Capital Territory', 'Australian Capital Territory'), ('Tasmania', 'Tasmania'), ('Western Australia', 'Western Australia')], max_length=20)),
                ('postcode', models.IntegerField()),
                ('DNSP', models.CharField(choices=[('Ausgrid', 'Ausgrid'), ('Citipower', 'Citipower'), ('Endeavour', 'Endeavour'), ('Energex', 'Energex'), ('Essential', 'Essential'), ('SAPN', 'SAPN'), ('Jemena', 'Jemena'), ('Powercor', 'Powercor'), ('Ausnet', 'Ausnet'), ('United Energy', 'United Energy'), ('Western Power', 'Western Power'), ('Horizon Power', 'Horizon Power'), ('ActewAGL', 'ActewAGL')], max_length=20)),
                ('Industry_type', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Mining', 'Mining'), ('Manufacturing', 'Manufacturing'), ('Electricity, Gas and Water Supply', 'Electricity, Gas and Water Supply'), ('Construction', 'Construction'), ('Wholesale Trade', 'Wholesale Trade'), ('Retail Trade', 'Retail Trade'), ('Accommodation, Cafes and Restaurants', 'Accommodation, Cafes and Restaurants'), ('Transport and Storage', 'Transport and Storage'), ('Communication Services', 'Communication Services'), ('Finance and Insurance', 'Finance and Insurance'), ('Property and Business Services', 'Property and Business Services'), ('Government Administration and Defence', 'Government Administration and Defence'), ('Education', 'Education'), ('Health and Community Services', 'Health and Community Services'), ('Cultural and Recreational Services', 'Cultural and Recreational Services'), ('Personal and Other Services', 'Personal and Other Services')], max_length=40)),
                ('default_solar_data', models.CharField(choices=[('Sydney', 'Sydney'), ('Melbourne', 'Melbourne'), ('Rockhampton', 'Rockhampton'), ('Adelaide', 'Adelaide'), ('Hobart', 'Hobart'), ('Perth', 'Perth'), ('Alice Springs', 'Alice Springs')], max_length=20)),
                ('program_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.Program')),
            ],
            options={
                'ordering': ('site_name',),
                'unique_together': {('program_name', 'site_name')},
            },
        ),
    ]
