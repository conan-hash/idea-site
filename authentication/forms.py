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



    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("با این آدرس ایمیل قبلا ثبت‌نام شده است")
        return email



class ProfileCompletionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'work_place', 'major', 'phone_number', 'national_id','personnel_number', 'job')
        widgets = {'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'minlength': 2,
                'maxlength': 255,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'minlength': 2,
                'maxlength': 255,
            }),
            'major': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'work_place': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'national_id': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'length': 10,
            }),
            'personnel_number': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }



class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'work_place', 'major', 'phone_number', 'national_id')