from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy


# To Automatically create One-to-One objects
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.
class MyUserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email Must be Set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)


from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(
        _("Staff Status"), 
        default=False,
        help_text=_("Designates whether the user can log in the site")
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active")
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']  # Add any additional required fields

    objects = MyUserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name or self.email  # Fallback to email if name is not set
    
    def get_short_name(self):
        return self.name or self.email
# Create your models here.
