from django.urls import path, re_path
from apps.ai_assistant.controllers.api.ai import (
    AIImproveDescriptionAPIView,
    AISuggestPriceAPIView,
    AISearchAssistAPIView,
    AIChatAPIView
)

urlpatterns = [
    re_path(r'^improve-description/?$', AIImproveDescriptionAPIView.as_view(), name='api_ai_improve_desc'),
    re_path(r'^suggest-price/?$', AISuggestPriceAPIView.as_view(), name='api_ai_suggest_price'),
    re_path(r'^search-assist/?$', AISearchAssistAPIView.as_view(), name='api_ai_search_assist'),
    re_path(r'^chat/?$', AIChatAPIView.as_view(), name='api_ai_chat'),
]
