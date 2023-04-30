import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, date_of_birth):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            is_active=True
        )

        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(blank=True, null=True, max_length=1)
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'date_of_birth']

    objects = MyUserManager()
