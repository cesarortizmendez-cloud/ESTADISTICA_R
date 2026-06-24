# -*- coding: utf-8 -*-
from django.shortcuts import render
from core.curriculum import nav_list, DATAFRAMES

def index(request):
    return render(request, "core/dataframes.html", {
        "df": DATAFRAMES,
        "chapters": nav_list(),
        "active": "dataframes",
    })
