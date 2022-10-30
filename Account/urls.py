from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import PasswordChangeDoneView

app_name = 'Account'

urlpatterns = [
    path('register', Register.as_view(), name='Register'),
    path('verify_register', UserRegisterVerifyCode.as_view(), name='user_register_verify'),
    path('Login', Login.as_view(), name='login'),
    path('Logout', Logout.as_view(), name='logout'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('delete_user/', DeleteAccountUser.as_view(), name='delete_user'),
    path('password_change', Password_change.as_view(), name='password_change'),
    path('password_change_done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/', UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('teacherlist', Teacherlist.as_view(), name='teacherlist'),
    path('detail/<int:pk>',Teacherprofile.as_view(),name='teacher_profile')

]
