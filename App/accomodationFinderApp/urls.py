from __future__ import absolute_import
from django.urls import path, include
from django.contrib import admin

from . import views
from . import home
from . import result

urlpatterns = [
    path('', home.HomeView.as_view(), name='index'),
    path('result/<uuid:id>', result.ResultView.as_view(), name='result')
]
