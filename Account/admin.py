from django.contrib import admin
from .models import User,Otp
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
        list_display = ('email','phonenumber', 'is_active', 'is_staff', 'is_admin','is_superuser','is_special_user','is_teacher')
        search_fields = ('email', 'phonenumber')



        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

admin.site.register(User,UserAdmin)



admin.site.register(Otp)
# Register your models here.


