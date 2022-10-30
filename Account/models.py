from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.urls import reverse
from django.utils import timezone
from extensions.utils import jalali_converter

class MyUserManager(BaseUserManager):
    def create_user(self, email,username,phonenumber,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phonenumber:
            raise ValueError('Users must have a phonenumber')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phonenumber=phonenumber

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username ,phonenumber, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phonenumber=phonenumber,
            username=username


        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True,verbose_name = "ایمیل")
    phonenumber = models.IntegerField(unique=True,null=True,blank=True,verbose_name = "شماره تلفن")
    image=models.ImageField(default='sutdent-prof.png',upload_to='profile_image',blank=True,null=True,verbose_name = "عکس کاربر" )
    bio = models.TextField(blank=True, null=True, verbose_name="درباره من:")
    special_user=models.DateTimeField(default=timezone.now, blank=True,null=True,verbose_name = "کابر ویژه")
    is_teacher=models.BooleanField(default=False, blank=True,null=True,verbose_name = "استاد")
    is_active = models.BooleanField(default=True,verbose_name = "فعال بودن حساب")
    is_admin = models.BooleanField(default=False,verbose_name = "امین")
    is_superuser = models.BooleanField(default=False,verbose_name = "ادمین_اصلی")


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phonenumber','username']

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean =True
    is_special_user.short_description = 'وضعیت کابر ویژه'


    def __str__(self):
        return  f'{self.email} and {self.phonenumber}'

    def jspecial_user(self):
        return jalali_converter(self.special_user)
    #
    #
    # def get_absolute_url(self):
    #     return reverse('self.image.url')

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff

        return self.is_admin

# Create your models here.








class Otp(models.Model):
    phonenumber=models.CharField(max_length=11,unique=True,verbose_name = "شماره تلفن")
    code=models.CharField(max_length=6,verbose_name = "کد تایید")
    created = models.DateTimeField(auto_now=True,verbose_name = "زمان ایجاد")




    def __str__(self):
        return f'{self.phonenumber},code={self.code}'

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کد های تایید"

