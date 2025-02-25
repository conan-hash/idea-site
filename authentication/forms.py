from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        # This method is called automatically during form validation
        email = self.cleaned_data.get('email').lower()  # Normalize email
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


class ProfileCompletionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'work_place', 'major', 'phone_number', 'national_id')