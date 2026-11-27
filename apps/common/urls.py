from django.urls import path
from apps.common.views import HomeView, set_language_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('set-language/<str:lang_code>/', set_language_view, name='set_language'),
]
