from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from countries.models import Country
import uuid

# Create your models here.
ACCOUNT_TYPE = [
    ("Business", "BUSINESS"),
    ("Individual", "INDIVIDUAL"),
]

JOB_STATUS = [
    ("Employed", "EMPLOYED"),
    ("Not Employed", "NOT EMPLOYED"),
]

EMPLOYMENT_TYPE = [
    ("Freelancer", "FREELANCER"),
    ("Full Time", "FULL TIME"),
    ("Part Time", "PART TIME"),
    ("Contract", "CONTRACT"),
    ("Seasonal Worker", "SEASONAL WORKER"),
    ("Self-employed", "SELF-EMPLOYED"),
]


class Industry(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Field is required")
        else:
            user = self.model(email=self.normalize_email(email),**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AppUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=50, unique=False, null=True, blank=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    job_status = models.CharField(max_length=50, choices=JOB_STATUS)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE)
    job_role = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    agree = models.BooleanField()
    email_verified = models.BooleanField(default=False)
    token_otp = models.PositiveIntegerField(null=True, blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "agree"]

    objects = AppUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.account_type} Account"
    
    def save(self, *args, **kwargs):
        if not self.token_otp:
            self.token_otp = str(uuid.uuid4()).replace('-', "").upper()[:6]
        return super().save(*args, **kwargs)
