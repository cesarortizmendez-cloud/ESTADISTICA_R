# -*- coding: utf-8 -*-
from django.shortcuts import render
from core.curriculum import nav_list

def index(request):
    return render(request, "core/transformador.html", {
        "chapters": nav_list(),
        "active": "transformador",
    })
