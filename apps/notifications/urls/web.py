from django.urls import path
from apps.notifications.views import (
    NotificationWebListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView
)

urlpatterns = [
    path('', NotificationWebListView.as_view(), name='notifications_list'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification_mark_read'),
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='notifications_mark_all_read'),
]
