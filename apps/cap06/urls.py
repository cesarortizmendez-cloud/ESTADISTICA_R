# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "cap06"
urlpatterns = [path("", views.index, name="index")]
