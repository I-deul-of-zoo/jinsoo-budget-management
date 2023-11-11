from django.urls import path
from budgets.views import CategoryListView

app_name = "budgets"
# base_url: api/budgets/

urlpatterns =[
    path("", CategoryListView.as_view())
]
