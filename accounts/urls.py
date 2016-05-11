from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login/$', views.UserLogin.as_view(), name="user_login"),
    url(r'register/$', views.UserRegister.as_view(), name="user_register"),
    url(r'delivery/$', views.UserDeliveryView.as_view(), name="user_delivery"),
    url(r'forgot/$', views.ForgotPassword.as_view(), name="forgot_password"),
    url(r'^myprofile/$', views.UserProfileView.as_view(), name='user_profile_page'),    
]
