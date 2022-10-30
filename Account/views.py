from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.views.generic import View, FormView, UpdateView,DeleteView,ListView,DetailView
from .forms import Password_Change, CheckOtpCodeForm, UserRegisterForm,ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Otp
from django.contrib import messages
from django.contrib.auth import views as auth_views
from utils import send_otp_code
from random import randint



class Register(View):
    form_class = UserRegisterForm
    template_name = 'Account/register.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:home')
        context = {
            'form': form
        }

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(100000, 999999)
            send_otp_code(cd['phonenumber'], random_code)
            Otp.objects.create(phonenumber=cd['phonenumber'], code=random_code)

            print(random_code)
            request.session['user_registration_info'] = {
                'email': cd['email'],
                'username': cd['username'],
                'phonenumber': cd['phonenumber'],
                'password': cd['password1']
            }

            messages.success(request, 'We send you a code', 'success')
            return redirect('Account:user_register_verify')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class UserRegisterVerifyCode(View):
    form_class = CheckOtpCodeForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, 'Account/Otp_cheker.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = Otp.objects.get(phonenumber=user_session['phonenumber'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(code_instance.code)
            if cd['code'] == str(code_instance.code):
                User.objects.create_user(
                    user_session['email'],
                    user_session['username'],
                    user_session['phonenumber'],
                    user_session['password']
                )

                code_instance.delete()
                messages.success(request, "You're registered.", 'success')
                return redirect('Account:login')
            else:
                messages.error(request, 'This code is wrong!', 'danger')
                return redirect('Account:user_register_verify')
        return redirect('Home:home')


class Login(LoginView):
    def get_success_url(self):
        return reverse_lazy('Home:home')


class Logout(LogoutView):
    def get_success_url(self):
        return reverse_lazy('Home:home')

#
class ProfileUser(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'Account/profile.html'
    success_url = reverse_lazy('Account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

class DeleteAccountUser(DeleteView):
    model = User
    template_name = 'Account/deleteuseraccount.html'


    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('Home:home')
class Teacherlist(ListView):
    model = User
    template_name = 'Account/teacherlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Teacher_list'] = User.objects.filter(is_teacher=True)
        # articles = Article.objects.filter(teacher=)
        return context

class Teacherprofile(DetailView):
    model = User
    template_name = 'Account/teacher_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Teacher'] = User.objects.filter(is_teacher=True)
        # articles = Article.objects.filter(teacher=)
        return context


class Password_Change(FormView):
    form_class = Password_Change
    template_name = 'Account/password_change.html'
    success_url = reverse_lazy('Account:password_change_done')


class Password_change(PasswordChangeView):
    def get_success_url(self):
        return reverse_lazy('Account:password_change_done')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'Account/password_reset.html'
    success_url = reverse_lazy('Account:password_reset_done')
    email_template_name = 'Account/Create password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'Account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'Account/password_reset_confirm.html'
    success_url = reverse_lazy('Account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'Account/password_reset_complete.html'
