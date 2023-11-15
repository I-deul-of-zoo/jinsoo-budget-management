from django.urls import path
from expenditures.views import ExpenditureView, ExpenditureListCreateView

app_name = "expenditures"
# base_url: api/expenditures/

urlpatterns =[
    path("", ExpenditureListCreateView.as_view()),
    # path("<int:ex_pk>/", ExpenditureView.as_view()),
]
