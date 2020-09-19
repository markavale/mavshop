from django.urls import path, include
from .views import (
    lightroom_view,
    photoshop_view,
        )


app_name = 'core'

urlpatterns = [
    #Lightroom
    path('lightroom-presets/', lightroom_view, name="lightroom"),
    
    #Photoshop
    path('photoshop-templates/', photoshop_view, name="photoshop"),

    # API VIEWs
    path('api/', include('core.api.urls')),
]
