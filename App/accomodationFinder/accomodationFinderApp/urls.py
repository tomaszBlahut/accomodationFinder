from __future__ import absolute_import
from django.urls import path

from . import views
from . import home

urlpatterns = [
    path('', home.HomeView.as_view(), name='index'),
]