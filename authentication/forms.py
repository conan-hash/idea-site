from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='ایمیل',
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید',
            'invalid': 'فرمت ایمیل نامعتبر است',
            'unique': 'این ایمیل قبلا ثبت شده است'
        }
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password1'].error_messages = {
            'required': 'لطفا رمز عبور را وارد کنید',
            'password_too_short': 'رمز عبور باید حداقل ۸ کاراکتر باشد',
            'password_too_common': 'رمز عبور بسیار ساده است',
            'password_entirely_numeric': 'رمز عبور نمی‌تواند فقط عدد باشد'
        }
        
        self.fields['password2'].error_messages = {
            'required': 'لطفا تکرار رمز عبور را وارد کنید',
            'password_mismatch': 'رمزهای عبور مطابقت ندارند'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("با این آدرس ایمیل قبلا ثبت‌نام شده است")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.fields['password2'].error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class ProfileCompletionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'work_place', 'major', 'phone_number', 'national_id')