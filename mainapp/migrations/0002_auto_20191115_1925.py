# Generated by Django 2.2.6 on 2019-11-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmodel',
            name='power_1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='power_2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='power_3',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='power_4',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=13),
        ),
    ]
