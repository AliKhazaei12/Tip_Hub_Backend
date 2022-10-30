# Generated by Django 4.1 on 2022-09-09 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otp',
            options={'verbose_name': 'کد تایید', 'verbose_name_plural': 'کد های تایید'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل ها'},
        ),
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.CharField(max_length=6, verbose_name='کد تایید'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='phonenumber',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='درباره من'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(blank=True, default='sutdent-prof.png', upload_to='profile_image', verbose_name='عکس کاربر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, default='', null=True, verbose_name='آدرس های شبکه های اجتماعی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال بودن حساب'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='امین'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='ادمین_اصلی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='استاد'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='user',
            name='special_user',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='کابر ویژه'),
        ),
    ]