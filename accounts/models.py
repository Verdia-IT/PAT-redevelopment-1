from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.exceptions import ValidationError
import os


# USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

def valid_email(email):
    if "verdia.com.au" not in email:
        raise ValidationError("Email is not valid for registeration")


class VerdiaUserManager(BaseUserManager):
    def create_user(self, email, password=None,  is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        

        user = self.model(
            email = self.normalize_email(email),            
        )
        # user.password = password # bad
        user.set_password(password)
        user.staff = is_staff
        user.active = is_active
        user.admin = is_admin
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(email,  password=password, is_admin=True, is_staff=True)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

class VerdiaUser(AbstractBaseUser):
    # username = models.CharField(max_length=300, unique=True,
    #                     validators=[RegexValidator(regex=USERNAME_REGEX, message='Username must be alphanumeric or contain numbers',
    #                     code='invalid_username')
    #                     ]
    #                 )
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address', validators=[valid_email])
    # full_name = models.CharField(max_length=255)
    staff = models.BooleanField(default=False) # 
    active = models.BooleanField(default=True) # can login
    admin = models.BooleanField(default=False) # superuser
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = VerdiaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff


class Profile(models.Model):
    user = models.OneToOneField(VerdiaUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True,upload_to='Profile/')

    def __str__(self):
        return self.user.email

    
   



