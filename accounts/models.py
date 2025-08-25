from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with role, and account expiry.
    Email or phone is the unique identifier.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        ECOPIA_STAFF = 'ECOPIA_STAFF', _('Ecopia_Staff')
        CUSTOMER = 'CUSTOMER', _('Customer')
        WASTE_PROVIDER = 'WASTE_PROVIDER', _('WASTE_PROVIDER')

    email = models.EmailField(_('email address'), unique=True)
    phone = PhoneNumberField(_("Phone number"), unique=True)
    full_name = models.CharField(max_length=300)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # ✅ Added missing field

    role_choice = models.CharField(

        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    date_joined = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True, help_text="Account expiry date/time")

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["full_name", "phone"]  
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role_choice == self.Role.ADMIN
    
    def is_ecopia_staff(self):
        return self.role_choice == self.Role.ECOPIA_STAFF
    
    def is_customer(self):
        return self.role_choice == self.Role.CUSTOMER

    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False

    def save(self, *args, **kwargs):
        if self.is_admin():
            self.is_staff = True
        super().save(*args, **kwargs)


class Profile(models.Model):
    """
    Extended user profile with additional information.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email


class AuditLog(models.Model):
    """
    Logs user activities for auditing and security purposes.
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_reset', 'Password Reset'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    description = models.TextField(blank=True, help_text="Optional details about the action")

    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.email if self.user else "Unknown User"
        return f"{user_str} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


# ✅ Auto-create profile when user is created
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
