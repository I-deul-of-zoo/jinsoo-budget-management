from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("username 필드는 필수 필드입니다.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    
    username = models.CharField(max_length=30, unique=True)
    email = None
    updated_at = models.DateTimeField(auto_now=True)
    total = models.PositiveIntegerField(default=0)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    


