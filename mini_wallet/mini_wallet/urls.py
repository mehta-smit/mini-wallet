"""mini_wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from wallet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/wallet', views.Wallet.as_view(), name='wallet'),
    path('api/v1/wallet/deposits', views.DepositMoney.as_view(), name='deposits'),
    path('api/v1/wallet/withdrawals', views.WithdrawalMoney.as_view(), name='withdrawal'),
    path('api/v1/init', views.Account.as_view(), name="account"),
    path('api/v1/send/otp', views.SendOTP.as_view(), name='generate_otp'),
    path('api/v1/verify/otp', views.VerifyAccount.as_view(), name='verify_otp')
]
