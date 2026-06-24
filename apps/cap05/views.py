# -*- coding: utf-8 -*-
from django.shortcuts import render
from core.curriculum import get_chapter, nav_list

CAP_NUM = 5

def index(request):
    ch = get_chapter(CAP_NUM)
    return render(request, "core/chapter.html", {
        "ch": ch,
        "chapters": nav_list(),
        "active": ch["slug"],
    })
