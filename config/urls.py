# -*- coding: utf-8 -*-
"""Rutas raiz del proyecto EstadisticaR."""
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("consola/", core_views.console, name="console"),
    path("ayuda-r/", core_views.cheatsheet, name="cheatsheet"),
    path("manifest.json", core_views.manifest, name="manifest"),
    path("service-worker.js", core_views.service_worker, name="service_worker"),

    # 11 capitulos = 11 apps
    path("cap/01/", include("apps.cap01.urls")),
    path("cap/02/", include("apps.cap02.urls")),
    path("cap/03/", include("apps.cap03.urls")),
    path("cap/04/", include("apps.cap04.urls")),
    path("cap/05/", include("apps.cap05.urls")),
    path("cap/06/", include("apps.cap06.urls")),
    path("cap/07/", include("apps.cap07.urls")),
    path("cap/08/", include("apps.cap08.urls")),
    path("cap/09/", include("apps.cap09.urls")),
    path("cap/10/", include("apps.cap10.urls")),
    path("cap/11/", include("apps.cap11.urls")),

    # modulos extra
    path("dataframes/", include("apps.dataframes.urls")),
    path("transformador/", include("apps.transformador.urls")),
]
