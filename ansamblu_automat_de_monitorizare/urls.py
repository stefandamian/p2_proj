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
from application.views import home_view, preturi_lista_chart, produse_view, add_lista_view, show_lista_view, show_produs_view, preturi_chart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('home/', home_view, name="home"),
    path('search/', add_lista_view, name="search"),
    path('produse/', produse_view, name="produse"),
    path('produs/<int:id>', show_produs_view, name="produs"),
    path('lista/<int:id>', show_lista_view, name="lista"),
    path('produs/<int:id>/preturi/', preturi_chart, name="preturi_produs"),
    path('produs/lista/<int:id>/', preturi_lista_chart, name="preturi_lista"),
]
