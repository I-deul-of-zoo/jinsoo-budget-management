from django.db import models
from django.contrib.auth import get_user_model

from budgets.models import Category

User = get_user_model()

class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    payment = models.PositiveIntegerField(default=0)
    appropriate_payment = models.PositiveIntegerField(default=5000)
    memo = models.TextField(null=True, blank=True)
    is_exept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
