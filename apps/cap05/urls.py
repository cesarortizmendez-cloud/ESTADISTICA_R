# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "cap05"
urlpatterns = [path("", views.index, name="index")]
