from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User, Otp
from ckeditor.widgets import CKEditorWidget


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'placeholder': ' تکرار گذرواژه'}))

    class Meta:
        model = User
        fields = ('email', 'phonenumber', 'username')
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'email-input', 'placeholder': 'پست الکترونیکی'}),
            'phonenumber': forms.TextInput(
                attrs={'class': 'integer-input', 'placeholder': 'شماره تماس'}),
            'username': forms.TextInput(
                attrs={'class': 'username-input', 'placeholder': 'نام کاربری'})

        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'phonenumber', 'is_active', 'is_admin')


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'پست الکترونیکی'}))
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )
    phonenumber = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'گذرواژه'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input1', 'dir': 'ltr', 'placeholder': 'تایید گذرواژه'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('This email already exists!')
        return email

    def clean_phone_number(self):
        phonenumber = self.cleaned_data['phonenumber']
        user = User.objects.filter(phonenumber=phonenumber)
        if user:
            raise ValidationError('This phone number already exists!')
        # Removed the duplicate code for this phone number
        Otp.objects.filter(phonenumber=phonenumber).delete()
        return phonenumber


class CheckOtpCodeForm(forms.Form):
    code = forms.CharField(label='کد', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'لطفا کد تایید را وراد کنید '}
    ))


class Password_Change(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control'})
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['phonenumber'].disabled = True
        self.fields['special_user'].disabled = True
        self.fields['is_teacher'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'phonenumber',
                  'first_name', 'last_name', 'special_user', 'is_teacher', 'bio']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'email-input', 'placeholder': 'پست الکترونیکی:'}),
            'phonenumber': forms.TextInput(
                attrs={'class': 'integer-input', 'placeholder': 'شماره تماس:'}),
            'username': forms.TextInput(
                attrs={'class': 'username-input', 'placeholder': 'نام کاربری:'}),
            'first_name': forms.TextInput(
                attrs={'class': 'username-input', 'placeholder': 'نام: '}),
            'last_name': forms.TextInput(
                attrs={'class': 'username-input', 'placeholder': 'نام خانوادگی:'}),


        }
