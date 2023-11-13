from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1)
    amount = models.PositiveIntegerField(default=0)
    ratio = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

CATEGORIES={
    "undefined": 1,
    "쇼핑": 2,
    "교통": 3,
    "주거비": 4,
    "취미": 5,
    "교육": 6,
    "병원": 7,
    "식비": 8,
    "저축/투자": 9,
}
REC_LIST = ["식비위주", "쇼핑위주", "취미위주", "저축/투자위주"]
BUDGET_REC_RATIO = {
    REC_LIST[0] : [
            {
                "category": CATEGORIES["쇼핑"],
                "ratio": 10,
            },
            {
                "category": CATEGORIES["식비"],
                "ratio": 40,
            },
            {
                "category": CATEGORIES["주거비"],
                "ratio": 25,
            },
            {
                "category": CATEGORIES["저축/투자"],
                "ratio": 15
            },
            {
                "category": CATEGORIES["취미"],
                "ratio": 10,
            },
        ],
    REC_LIST[1] : [
            {
                "category": CATEGORIES["쇼핑"],
                "ratio": 35,
            },
            {
                "category": CATEGORIES["식비"],
                "ratio": 25,
            },
            {
                "category": CATEGORIES["주거비"],
                "ratio": 20,
            },
            {
                "category": CATEGORIES["취미"],
                "ratio": 10,
            },
            {
                "category": CATEGORIES["교통"],
                "ratio": 10,
            },
        ],
    REC_LIST[2] : [
            {
                "category": CATEGORIES["쇼핑"],
                "ratio": 15,
            },
            {
                "category": CATEGORIES["식비"],
                "ratio": 25,
            },
            {
                "category": CATEGORIES["주거비"],
                "ratio": 20,
            },
            {
                "category": CATEGORIES["취미"],
                "ratio": 20,
            },
        ],
    REC_LIST[3] : [
            {
                "category": CATEGORIES["쇼핑"],
                "ratio": 10,
            },
            {
                "category": CATEGORIES["식비"],
                "ratio": 30,
            },
            {
                "category": CATEGORIES["주거비"],
                "ratio": 20,
            },
            {
                "category": CATEGORIES["저축/투자"],
                "ratio": 30,
            },
            {
                "category": CATEGORIES["교통"],
                "ratio": 10,
            },
        ]
}
