from django.urls import path
from apps.ai_assistant.controllers.web.ai import AIAssistantPageView

urlpatterns = [
    path('', AIAssistantPageView.as_view(), name='ai_assistant_page'),
]
