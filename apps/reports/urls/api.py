from django.urls import path
from apps.reports.controllers.api.reports import ReportCreateAPIView

urlpatterns = [
    path('', ReportCreateAPIView.as_view(), name='api_reports_create'),
]
