# Generated by Django 4.1 on 2022-09-07 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='article',
            new_name='Article',
        ),
    ]