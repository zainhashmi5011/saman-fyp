# Generated by Django 4.0.4 on 2023-05-19 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_academicexp__from_academicexp__to_achievements__from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bg_color',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
