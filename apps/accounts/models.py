from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractUser):
    phone_number = models.CharField(_('Phone_number'),max_length=11, unique=True)
    address = models.TextField(_('Address'),)
    email = models.EmailField(_('Email'), max_length=100, unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        error_messages={
            "unique": _("A user with that username already exists."),
        },blank=True,
        null=True, )

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class VerificationOTP(models.Model):
    class VerificationType(models.TextChoices):
        REGISTER = 'register',_('Register')
        RESET_PASSWORD = 'reset_password',_('Reset Password')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_otp')
    code = models.IntegerField(_('OTP Code'))
    type = models.CharField(_('OTP Type'), max_length=30, choices=VerificationType.choices)
    expires_in = models.DateTimeField(_('Expiration In'))

    def __str__(self):
        return f'{str(self.user.email)} {self.code}'

    class Meta:
        verbose_name = _('Verification OTP')
        verbose_name_plural = _('Verification OTPs')


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    name = models.CharField(_('Name'), max_length=200)
    phone_number = models.CharField(_('Phone_number'), max_length=15)
    apartment = models.CharField(_('Apartment'), max_length=200)
    street = models.TextField(_('Street'))
    #city = models.ForeignKey()
    pincode = models.CharField(_('Pincode'), max_length=50)

    def __str__(self):
        return f'{self.user.email} {self.name}'

    class Meta:
        verbose_name = _('User Address')
        verbose_name_plural = _('User Addresses')