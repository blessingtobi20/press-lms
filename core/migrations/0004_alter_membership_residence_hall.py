# Generated by Django 4.0.6 on 2022-10-12 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_membership_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='residence_hall',
            field=models.CharField(blank=True, choices=[('Abigail', 'Abigail'), ('Abraham', 'Abraham'), ('Daniel', 'Daniel'), ('Deborah', 'Deborah'), ('Dorcas', 'Dorcas'), ('Isaac', 'Isaac'), ('Joseph', 'Joseph'), ('Sarah', 'Sarah')], max_length=20, null=True),
        ),
    ]
