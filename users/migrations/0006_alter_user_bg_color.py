# Generated by Django 4.0.4 on 2023-05-19 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_bg_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bg_color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=2000, null=True),
        ),
    ]