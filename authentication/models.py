from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email is the unique identifier
    is_verified = models.BooleanField(default=False)  # Email verification flag
    email_token = models.CharField(max_length=100, null=True, blank=True)  # Verification token
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    work_place = models.CharField(max_length=255, null=True)
    job = models.CharField(max_length=255, null=True)
    major = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    national_id = models.CharField(max_length=10, null=True)
    personnel_number = models.CharField(max_length=10, null=True, blank=True)

    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    username = None  # Remove the username field

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = []  # No additional fields required for createsuperuser
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_email_token(self):
        self.email_token = str(uuid.uuid4())
        self.save()
        return self.email_token


