from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)

# Create your models here.

class UserManager(BaseUserManager):
    """Custom model user manager."""

    def create_user(self, username, email, password=None):
        """Override create user method for customized user model."""
        
        if username is None:
            raise TypeError('Users must have username.')

        if email is None:
            raise TypeError('Users must have email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        """Override create superuser method for customized user model."""
        
        if password is None:
            raise TypeError('Password should not be empty.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

