from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'


def get_default_profile_image_filepath():
    return 'account_24dp.svg'


class AccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, mobile_number, password=None):
        if not email:
            raise ValueError("Users must have an Email address")
        if not username:
            raise ValueError("Users must have an Username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not mobile_number:
            raise ValueError("Users must have a mobile number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, mobile_number, password=None):

        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    # AbstractBaseUser class already has id, password & last login also update USERNAME_FIELD for unique identifier needed

    email = models.EmailField(verbose_name="Email Id",
                              max_length=60, unique=True)
    username = models.CharField(
        verbose_name="Username", max_length=30, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    mobile_number = models.CharField(
        verbose_name="Mobile Number", max_length=10, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="Date Joined", auto_now_add=True)
    is_admin = models.BooleanField(default="False")
    is_active = models.BooleanField(default="False")
    is_staff = models.BooleanField(default="False")
    is_superuser = models.BooleanField(default="False")
    is_paid = models.BooleanField(default="False")
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                      null=True, blank=True, default=get_default_profile_image_filepath)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'mobile_number']

    objects = AccountManager()

    def __str__(self):
        return self.username

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # @property
    # def is_admin(self):
    #     return self.is_admin

    # @property
    # def is_staff(self):
    #     return self.is_staff

    # @property
    # def is_active(self):
    #     return self.is_active

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # def get_short_name(self):
    #     return self.first_name

    # def get_full_name(self):
    #     return self.full_name

    def get_profile_image_filename(self):
        return str(self.profile_image[str(self.profile_image.index(f'profile_images/{self.pk}/')):])

    # email or EMAIL_FIELD will be returned by internal get_email_field_name() method


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
