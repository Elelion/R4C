"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

import home
from robots import views as robots_views
from orders import views as orders_views
from home import views as home_views


urlpatterns = [
    # Включить админку
    path('admin/', admin.site.urls),

    # Включить URL-шаблоны для авторизации
    # path('accounts/login/', include('django.contrib.auth.urls')),
    path('home/', home_views.home_page, name='home'),
    path('login/', robots_views.login, name='login'),
    # path('logout/', robots_views.logout, name='logout'),


    # **


    # robots
    path('request_robot/', robots_views.request_robot, name='request_robot'),
    path('download_robot_summary/', robots_views.download_robot_summary, name='download_robot_summary'),

    # orders
    path('create_order/<int:robot_id>/', orders_views.create_order, name='create_order'),
    path('view_orders/', orders_views.view_orders, name='view_orders'),
]
