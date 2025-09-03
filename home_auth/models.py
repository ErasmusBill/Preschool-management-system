from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)

    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",
        blank=True
    )
    USERNAME_FIELD = "email"   
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return f"{self.username} ({self.role})"
    
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        super().save(*args, **kwargs)

    def is_valid(self):
        expiration_time = self.created_at + timezone.timedelta(hours=1)
        return timezone.now() < expiration_time and not self.is_used

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/authentication/reset-password/{self.token}/"
        subject = "Password Reset Request"
        message = f"Click the link below to reset your password:\n{reset_link}\nThis link will expire in 1 hour."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.user.email])

    def __str__(self):
        return f"PasswordResetRequest for {self.user.email} at {self.created_at}"
