from django.urls import path
from expenditures.views import ExpenditureView

app_name = "expenditures"
# base_url: api/expenditures/

urlpatterns =[
    path("", ExpenditureView.as_view()),
]
