"""
Root URL Configuration for UMUM Platform
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseNotFound
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def admin_honeypot_view(request, *args, **kwargs):
    """
    Decoy Honeypot: catches unauthorized bots and scanners trying /admin/
    Logs the security breach attempt into AuditLog and returns 404.
    """
    try:
        from apps.audit.models import AuditLog
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action='UNAUTHORIZED_ADMIN_SCAN_BLOCKED',
            entity='admin_honeypot',
            ip_address=ip.split(',')[0].strip() if ip else None,
            extra_data={
                'attempted_path': request.path,
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown')
            }
        )
    except Exception:
        pass
    return HttpResponseNotFound(
        "<div style='font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;text-align:center;padding:80px 20px;'>"
        "<h1 style='font-size:3rem;margin-bottom:10px;color:#dc3545;'>404</h1>"
        "<h3 style='color:#333;margin-bottom:15px;'>Sahifa topilmadi yoki kirish taqiqlangan</h3>"
        "<p style='color:#777;max-width:500px;margin:0 auto 25px;'>Ushbu manzil mavjud emas. Xavfsizlik maqsadida barcha so‘rovlar jurnalga yozib borilmoqda.</p>"
        "<a href='/' style='display:inline-block;padding:10px 24px;background:#0d6efd;color:#fff;text-decoration:none;border-radius:20px;font-weight:600;'>Bosh sahifaga qaytish</a>"
        "</div>"
    )

# Secure Obfuscated Admin Path (FR-20 Security Hardening)
ADMIN_SECRET_PATH = getattr(settings, 'DJANGO_ADMIN_URL', 'portal-manager-7x9q/').strip('/') + '/'

urlpatterns = [
    # Decoy Honeypot on old /admin/ path
    re_path(r'^admin(/.*)?$', admin_honeypot_view, name='admin_honeypot'),

    # Real Secure Admin Portal
    path(ADMIN_SECRET_PATH, admin.site.urls),

    # OpenAPI 3 / Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # REST API v1
    path('api/v1/auth/', include('apps.accounts.urls.api_auth')),
    path('api/v1/users/', include('apps.accounts.urls.api_users')),
    path('api/v1/categories/', include('apps.categories.urls')),
    path('api/v1/listings/', include('apps.listings.urls.api')),
    path('api/v1/favorites/', include('apps.favorites.urls.api')),
    path('api/v1/chats/', include('apps.chats.urls.api')),
    path('api/v1/orders/', include('apps.orders.urls.api')),
    path('api/v1/payments/', include('apps.payments.urls.api')),
    path('api/v1/notifications/', include('apps.notifications.urls.api')),
    path('api/v1/ai/', include('apps.ai_assistant.urls.api')),
    path('api/v1/reports/', include('apps.reports.urls.api')),
    path('api/v1/moderation/', include('apps.moderation.urls.api')),
    path('api/v1/admin/', include('apps.analytics.urls.api')),

    # Django Templates Website URLs
    path('', include('apps.common.urls')),
    path('auth/', include('apps.accounts.urls.web_auth')),
    path('profile/', include('apps.accounts.urls.web_profile')),
    path('listings/', include('apps.listings.urls.web')),
    path('favorites/', include('apps.favorites.urls.web')),
    path('search/', include('apps.search.urls')),
    path('chats/', include('apps.chats.urls.web')),
    path('payments/', include('apps.payments.urls.web')),
    path('notifications/', include('apps.notifications.urls.web')),
    path('ai-assistant/', include('apps.ai_assistant.urls.web')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
