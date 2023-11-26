from django.urls import path
from expenditures.views import (
    ExpenditureView, 
    ExpenditureListCreateView, 
    ExpenditureRecommendToday, 
    ExpenditureNotificationToday,
    ExpenditureStatisticsData,
)

app_name = "expenditures"
# base_url: api/expenditures/

urlpatterns =[
    path("", ExpenditureListCreateView.as_view()),
    path("<int:ex_pk>/", ExpenditureView.as_view()),
    path("rec/", ExpenditureRecommendToday.as_view()),
    path("noti/", ExpenditureNotificationToday.as_view()),
    path("statistics/", ExpenditureStatisticsData.as_view()),
]
