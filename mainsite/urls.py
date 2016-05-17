from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="home_url"),
    url(r'shop/', include('shop.urls')),
    url(r'accounts/', include('accounts.urls')),
    
]
