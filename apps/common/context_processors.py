from django.conf import settings
from django.utils import translation
from apps.common.translations import UI_TRANSLATIONS

def common_context(request):
    """
    Global template context processor (FR-19).
    Detects language from:
    1. Query param ?lang=uz|ru|en
    2. Session
    3. Cookie
    4. Default 'uz'
    """
    lang_param = request.GET.get('lang')
    if lang_param and lang_param in UI_TRANSLATIONS:
        request.session['django_language'] = lang_param
        request.session.modified = True
        lang = lang_param
    else:
        lang = request.session.get('django_language') or request.COOKIES.get(getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')) or 'uz'

    if lang not in UI_TRANSLATIONS:
        lang = 'uz'

    translation.activate(lang)
    t = UI_TRANSLATIONS[lang]

    from apps.categories.models import Category
    try:
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')[:12]
    except Exception:
        categories = []

    unread_notifications_count = 0
    recent_notifications = []
    favorites_count = 0
    if request.user.is_authenticated:
        try:
            from apps.notifications.models import Notification
            user_notifs = Notification.objects.filter(user=request.user)
            unread_notifications_count = user_notifs.filter(is_read=False).count()
            recent_notifications = list(user_notifs[:6])
            favorites_count = request.user.favorites.count()
        except Exception:
            pass

    return {
        'SITE_NAME': 'UMUM',
        'SITE_TAGLINE': t['tagline'],
        'root_categories': categories,
        'current_language': lang,
        't': t,
        'unread_notifications_count': unread_notifications_count,
        'recent_notifications': recent_notifications,
        'favorites_count': favorites_count,
    }
