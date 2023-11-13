from django.urls import path
from budgets.views import BudgetsView, BudgetRecommendView

app_name = "budgets"
# base_url: api/budgets/

urlpatterns =[
    # path("", CategoryListView.as_view()),
    path("", BudgetsView.as_view()),
    path("rec/", BudgetRecommendView.as_view()),
]
