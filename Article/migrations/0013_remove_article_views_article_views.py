# Generated by Django 4.1 on 2022-09-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0012_ipaddress_remove_article_views_article_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='views',
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveBigIntegerField(default=2, verbose_name='بازدید ها'),
        ),
    ]
