from django.contrib import admin
from django.urls import path
from webEmobot.settings import USE_I18N
from .import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'emobot'

urlpatterns = [
    path('home/', views.homeView.as_view(), name="home"),
    path('dashboard/', views.dashboardView.as_view(), name="dashboard"),
    path('login/', views.loginView.as_view(), name="login"), 
    path('logout/', views.logoutView.as_view(), name="logout"), 
    path('register/', views.registerView.as_view(), name="register"),
    path('user/', views.userView.as_view(), name="user"),
    path('activate/', views.activateView.as_view(), name="activate"),
    path('forgot-password/', views.forgotpassowrdView.as_view(), name="forgot-password"),
    path('terms-and-conditions/', views.termsandconditionsView.as_view(), name="terms-and-conditions"),
    path('settings/account-settings', views.accountsettingsView.as_view(), name="account-settings"),
    path('settings/change-password', views.changepasswordView.as_view(), name="change-password"),
    path('settings/public-profile', views.publicprofileView.as_view(), name="public-profile"),
    path('settings/account-settings/delete-account', views.deleteaccountsView.as_view(), name="delete-account"),
    path('export_csv1', views.export_csv1, name="export_csv1"),
    path('export_csv2', views.export_csv2, name="export_csv2"),





]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)