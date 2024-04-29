from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserRole(Enum):
    DONOR = 'donor'
    CHARITY = 'charity'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, choices=[(role.value, role.name) for role in UserRole])
    ein_number = models.CharField(max_length=255, blank=True)
    image_data = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)  # optional email field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class Charity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)