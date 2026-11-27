from django.urls import path
from apps.accounts.controllers.web.profile import ProfileView, SellerProfileView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('seller/', SellerProfileView.as_view(), name='seller_profile'),
]
