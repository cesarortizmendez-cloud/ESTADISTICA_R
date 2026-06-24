# -*- coding: utf-8 -*-
"""
Indice central del curriculo. Combina los 11 capitulos y expone helpers
para que cada app Django obtenga su capitulo por numero/slug.
Tambien define el modulo extra de DataFrames y Mineria de Datos.
"""
from .curriculum_a import CHAPTERS_A
from .curriculum_b import CHAPTERS_B

CHAPTERS = CHAPTERS_A + CHAPTERS_B
BY_NUM = {c["num"]: c for c in CHAPTERS}
BY_SLUG = {c["slug"]: c for c in CHAPTERS}


def get_chapter(num):
    """Devuelve el dict del capitulo por su numero (1..11)."""
    return BY_NUM[num]


def nav_list():
    """Lista ligera para el menu lateral / home."""
    return [
        {"num": c["num"], "slug": c["slug"], "code": c["code"],
         "title": c["title"], "subtitle": c["subtitle"]}
        for c in CHAPTERS
    ]


# ====================================================================
#  MODULO EXTRA:  DATA FRAMES + MINERIA DE DATOS
# ====================================================================
DATAFRAMES = {
    "title": "Data Frames & Minería de Datos",
    "subtitle": "La tabla como objeto: el corazón del análisis de datos en R",
    "intro": """
<p>Un <b>data frame</b> es la estructura más importante de R: una <b>tabla</b> donde cada
<b>columna</b> es una variable (un vector) y cada <b>fila</b> es una observación. Es,
literalmente, una hoja Excel viviendo dentro de R. Todo el análisis de datos —frecuencias, gráficos,
correlación, modelos— opera sobre data frames.</p>
<p>La <b>minería de datos</b> es el proceso de descubrir patrones útiles en grandes volúmenes
de datos: limpieza, exploración, agrupación, detección de atípicos y modelos predictivos.
Aquí verás los primeros pasos con herramientas base de R.</p>
""",
    "blocks": [
        {
            "id": "anatomia",
            "title": "1 · Anatomía de un data frame",
            "explain": "Creamos una tabla, inspeccionamos su estructura y accedemos a filas y columnas.",
            "code": 'df <- data.frame(\n  nombre = c("Ana","Luis","Eva","Tomas","Sol"),\n  edad   = c(23, 31, 28, 45, 19),\n  area   = c("Prod","Calidad","Prod","Logist","Calidad"),\n  sueldo = c(680, 920, 710, 1300, 540)\n)\nstr(df)        # estructura: tipos de cada columna\ndim(df)        # filas x columnas\nhead(df, 3)    # primeras filas',
        },
        {
            "id": "acceso",
            "title": "2 · Seleccionar y filtrar",
            "explain": "df[fila, columna] o df$columna. Filtramos con condiciones lógicas.",
            "code": 'df <- data.frame(nombre=c("Ana","Luis","Eva","Tomas","Sol"),\n  edad=c(23,31,28,45,19), area=c("Prod","Calidad","Prod","Logist","Calidad"),\n  sueldo=c(680,920,710,1300,540))\ndf$sueldo                       # una columna\ndf[df$sueldo > 700, ]           # filas con sueldo > 700\ndf[df$area == "Prod", c("nombre","sueldo")]  # filtro + columnas',
        },
        {
            "id": "mutar",
            "title": "3 · Crear y transformar columnas",
            "explain": "Agregamos variables derivadas, base de la ingeniería de características (feature engineering).",
            "code": 'df <- data.frame(nombre=c("Ana","Luis","Eva","Tomas","Sol"),\n  edad=c(23,31,28,45,19), sueldo=c(680,920,710,1300,540))\ndf$sueldo_anual <- df$sueldo * 12\ndf$rango_edad <- cut(df$edad, breaks = c(0,25,35,100),\n                     labels = c("Joven","Adulto","Senior"))\ndf',
        },
        {
            "id": "agregar",
            "title": "4 · Agrupar y resumir (group by)",
            "explain": "aggregate() resume por grupos: el patrón split-apply-combine de la minería de datos.",
            "code": 'df <- data.frame(area=c("Prod","Calidad","Prod","Logist","Calidad"),\n  sueldo=c(680,920,710,1300,540), edad=c(23,31,28,45,19))\naggregate(sueldo ~ area, data = df, FUN = mean)\naggregate(cbind(sueldo, edad) ~ area, data = df, FUN = mean)',
        },
        {
            "id": "limpieza",
            "title": "5 · Limpieza de datos (NA y duplicados)",
            "explain": "El 80% de la minería es limpiar. Detectamos y tratamos faltantes y duplicados.",
            "code": 'df <- data.frame(x = c(10, NA, 12, 10, 99),\n                 y = c(1, 2, NA, 1, 3))\nis.na(df)                       # mapa de faltantes\ncolSums(is.na(df))              # NA por columna\ndf_clean <- na.omit(df)         # elimina filas con NA\ndf_clean[!duplicated(df_clean), ]  # quita duplicados',
        },
        {
            "id": "explorar",
            "title": "6 · Exploración multivariada (EDA)",
            "explain": "summary() y la matriz de correlación dan una foto completa de un dataset real.",
            "code": 'data(mtcars)\nsummary(mtcars[, c("mpg","hp","wt","qsec")])\nround(cor(mtcars[, c("mpg","hp","wt","qsec")]), 2)',
        },
        {
            "id": "outliers",
            "title": "7 · Detección de atípicos (minería)",
            "explain": "Regla del rango intercuartílico (IQR) para marcar valores anómalos.",
            "code": 'set.seed(1)\nx <- c(rnorm(50, 50, 5), 5, 95)   # dos atipicos inyectados\nq <- quantile(x, c(.25,.75))\niqr <- diff(q)\nlim <- c(q[1] - 1.5*iqr, q[2] + 1.5*iqr)\natipicos <- x[x < lim[1] | x > lim[2]]\ncat("Limites:", round(lim,1), "\\n")\ncat("Atipicos detectados:", round(atipicos,1), "\\n")\nboxplot(x, horizontal = TRUE, col = "#22d3ee", main = "Deteccion de atipicos")',
        },
        {
            "id": "clustering",
            "title": "8 · Agrupamiento con k-means (minería)",
            "explain": "k-means descubre grupos naturales sin etiquetas. Aquí, 3 clusters sobre iris.",
            "code": 'data(iris)\nset.seed(2024)\nX <- iris[, c("Petal.Length","Petal.Width")]\nkm <- kmeans(X, centers = 3)\nplot(X, col = c("#00ff9c","#22d3ee","#ff2e97")[km$cluster],\n     pch = 19, main = "k-means sobre iris (3 grupos)",\n     xlab = "Largo del petalo", ylab = "Ancho del petalo")\npoints(km$centers, pch = 8, cex = 2, lwd = 2)\ntable(cluster = km$cluster, especie = iris$Species)',
        },
    ],
    "exercises": [
        "Crea un data frame de 5 productos con precio y stock; agrega una columna 'valor = precio*stock'.",
        "Sobre <code>mtcars</code>, calcula el mpg promedio agrupado por número de cilindros con <code>aggregate()</code>.",
        "Detecta atípicos en <code>mtcars$hp</code> con la regla del IQR.",
        "Aplica <code>kmeans()</code> con 2 centros sobre <code>mtcars[,c('mpg','wt')]</code> y grafica los grupos.",
    ],
}
