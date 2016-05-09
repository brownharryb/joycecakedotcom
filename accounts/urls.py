from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login/', views.UserLogin.as_view(), name="user_login"),
    url(r'forgot/', views.ForgotPassword.as_view(), name="forgot_password"),    
]
