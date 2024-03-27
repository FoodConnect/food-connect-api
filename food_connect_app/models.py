from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserRole(Enum):
    DONOR = 'donor'
    CHARITY = 'charity'

class CartStatus(Enum):
    CARTED = 'carted'
    ORDERED = 'ordered'

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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[(role.value, role.name) for role in UserRole])
    ein_number = models.CharField(max_length=255)
    image_data = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

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

class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image_data = models.CharField(max_length=255)
    description = models.TextField()
    total_inventory = models.IntegerField()
    claimed_inventory = models.IntegerField(default=0)
    remaining_inventory = models.IntegerField()
    pick_up_deadline = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[(status.value, status.name.title()) for status in CartStatus])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartedDonation(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    donation_receipt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DonationCategory(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

