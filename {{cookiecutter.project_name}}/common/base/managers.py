from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class SiteUserManager(BaseUserManager):
    """
    this User manager is different from the default one by this that a username does not exist.
    the login and primary key field is the email.
    """

    def create_user(self, email, password=None, **extra_fields):
        today = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')

        email = SiteUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u
