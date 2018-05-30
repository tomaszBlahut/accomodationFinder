from __future__ import absolute_import
from django.urls import path, include
from django.contrib import admin

from . import views
from . import home
from . import place

urlpatterns = [
    path('', home.HomeView.as_view(), name='index'),
    path('/<int:UUID>', place.HomeView2.as_view(), name='place')
]

