# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "cap02"
urlpatterns = [path("", views.index, name="index")]
