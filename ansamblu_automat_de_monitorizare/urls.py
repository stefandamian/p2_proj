"""ansamblu_automat_de_monitorizare URL Configuration

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
from application.views import user_profile_view, register_view, reset_password_done_view, logout_view, home_view, preturi_lista_chart, produse_view, add_lista_view, show_lista_view, show_produs_view, preturi_chart
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), 
        name="login"),
    path('accounts/logout/', logout_view, name="logout"),
    path('accounts/register/', register_view, name="register"),
    path('accounts/profile/', user_profile_view, name='user_profile'),
    
    
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), 
        name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), 
        name='password_change_done'),
        
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(),
    	   name='password_reset'), # form with mail
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
    	   name='password_reset_done'), # message that the mail is sent
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
    	  name='password_reset_confirm'), # form for the change of password (form with pass and confirm pass)
    path('accounts/password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'), # message with reset of the password succesfull
     
    path('', home_view, name="home"),
    path('home/', home_view, name="home"),
    path('search/', add_lista_view, name="search"),
    path('produse/', produse_view, name="produse"),
    path('produs/<int:id>', show_produs_view, name="produs"),
    path('lista/<int:id>', show_lista_view, name="lista"),
    path('produs/<int:id>/preturi/', preturi_chart, name="preturi_produs"),
    path('produs/lista/<int:id>/', preturi_lista_chart, name="preturi_lista"),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    
]
