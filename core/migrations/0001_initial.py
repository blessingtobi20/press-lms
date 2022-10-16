# Generated by Django 4.0.6 on 2022-10-11 20:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=15)),
                ('reg', models.CharField(blank=True, max_length=50, null=True)),
                ('current_level', models.CharField(blank=True, choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500')], max_length=2000, null=True)),
                ('residence_hall', models.CharField(blank=True, choices=[('Abigail', 'Abigail'), ('Abraham', 'Abraham'), ('Daniel', 'Daniel'), ('Deborah', 'Deborah'), ('Dorcas', 'Dorcas'), ('Isaac', 'Isaac'), ('Daniel', 'Daniel'), ('Joseph', 'Joseph'), ('Sarah', 'Sarah')], max_length=20, null=True)),
                ('room', models.CharField(blank=True, max_length=5, null=True)),
                ('college', models.CharField(blank=True, choices=[('College of Pure and Applied Sciences', 'College of Pure and Applied Sciences'), ('College of Engineering', 'College of Engineering'), ('College of Business and Social Sciences', 'College of Business and Social Sciences'), ('College of Agricultural Sciences', 'College of Agricultural Sciences')], max_length=500, null=True)),
                ('department', models.CharField(blank=True, max_length=500, null=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=250)),
                ('message', models.CharField(max_length=5000)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.membership')),
            ],
        ),
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(max_length=1000)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='core.book')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrowed', models.DateField(default=datetime.datetime.now)),
                ('date_to_be_returned', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_book', to='core.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_book', to='core.membership')),
                ('copy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_book_copy', to='core.copy')),
            ],
        ),
    ]
