from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from login import views as login_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name="login/login.html"), name="login"),
    path('sku_modal/', login_views.sku_modal, name='sku_modal'),
    path('sku_save/', login_views.sku_save, name='sku_save'),
    path('view_sku/', login_views.view_sku, name='view_sku'),
    path('delete/<int:id>/', login_views.delete_data, name='delete_data'),
    # path('<int:id>/', login_views.update_data, name='update_data'),
    path('update_data/<int:id>/', login_views.update_data, name="update_data"),
    path('view_sku_ajax/', login_views.view_sku_ajax, name='view_sku_ajax'),
    path('search/', login_views.search, name='search'),

    path('sku_setting/', login_views.sku_setting, name='sku_setting'),
    path('sku_setting_save/', login_views.sku_setting_save, name='sku_setting_save'),
    path('view_setting/', login_views.view_setting, name='view_setting'),
    path('view_sku_country/', login_views.view_sku_country, name='view_sku_country'),
    path('view_setting_ajax/', login_views.view_setting_ajax, name='view_setting_ajax'),


    path('logout', auth_views.LogoutView.as_view(template_name="login/logout.html"), name="logout"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='login/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='login/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='login/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='login/password_reset_complete.html'
         ),
         name='password_reset_complete'),


]
