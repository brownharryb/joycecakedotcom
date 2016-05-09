from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index_view),
    url(r'shop/', include('shop.urls')),
    url(r'accounts/', include('accounts.urls')),
    
]
