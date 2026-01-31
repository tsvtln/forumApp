from django.db import models
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import unicodedata
from .managers import AppUserManager


# class CustomUser(AbstractUser):
#     points = models.IntegerField(default=0)


class AppUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'  # USERNAME_FIELD means the first credential in our auth
    REQUIRED_FIELDS = ['username']

    objects = AppUserManager()  # Set custom manager

    @classmethod
    def normalize_username(cls, username):
        """
        Normalize the username by applying Unicode normalization.
        This helps prevent homograph attacks and ensures consistent username storage.
        """
        if not username:
            return username
        return unicodedata.normalize('NFKC', username)

    @property
    def display_name(self):
        """
        Return a friendly display name for the user.
        Returns username if available, otherwise the email prefix (part before @).
        """
        if self.username and self.username != self.email:
            return self.username
        if self.email:
            return self.email.split('@')[0]
        return 'User'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
    )

    age = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    points = models.IntegerField(default=0)


# Note: Proxy models can't add new fields, they can only change behavior
# This is commented out because it would create a proxy of CustomUser
# class CustomProxyModel(CustomUser):
#     class Meta:
#         proxy = True

# class CustomProxyModel(CustomUser):
#     def custom_method(self):
#         return f'This is a custom method'
#
#     class Meta:
#         proxy = True


