from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email
from users.api.views import UserDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', include('users.urls', namespace='users')),
    path('', include('pages.urls', namespace='pages')),
    path('', include('core.urls', namespace='core')),
    path('confirm-email/', UserDetailView.as_view()),

   # path('rest-auth/', include('rest_auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
