from django.urls import path
from apps.search.views import SearchResultsView

urlpatterns = [
    path('', SearchResultsView.as_view(), name='search'),
]
