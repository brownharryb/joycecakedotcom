from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login/$', views.UserLogin.as_view(), name="user_login"),
    url(r'logout/$', views.logout_view, name="user_logout"),
    url(r'register/$', views.UserRegister.as_view(), name="user_register"),
    url(r'delivery/$', views.UserDeliveryView.as_view(), name="user_delivery"),
    url(r'forgot/$', views.ForgotPassword.as_view(), name="forgot_password"),
    url(r'recover_password/(?P<username>[\w-]+)/(?P<recovery_key>[\w-]+)/$', views.RecoverPasswordView.as_view(), name="recover_password"),
    url(r'^myprofile/$', views.UserProfileView.as_view(), name='user_profile_page'),
    url(r'changemypass/$', views.PasswordChangeOnProfile.as_view(), name="change_my_password"),
    url(r'^mytransaction/$', views.UserTransactionView.as_view(), name='user_transaction_page'),
]
