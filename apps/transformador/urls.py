# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "transformador"
urlpatterns = [path("", views.index, name="index")]
