# Generated by Django 4.1 on 2022-09-18 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0015_delete_ipaddress'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
