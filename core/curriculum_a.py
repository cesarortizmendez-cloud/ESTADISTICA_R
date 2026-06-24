# -*- coding: utf-8 -*-
"""
Contenido educativo de los Apuntes 1 a 6.
Cada capítulo es un dict con:
  num, slug, code, title, subtitle, apunte
  concepts  -> lista de (termino, definicion)
  theory    -> HTML didactico
  examples  -> lista de dicts {title, explain, code}  (R ejecutable en WebR / base R)
  dataset   -> nombre de un dataset R base usado de ejemplo
  exercises -> lista de retos para el alumno
"""

CHAPTERS_A = [
    # ============================================================ CAP 01
    {
        "num": 1,
        "slug": "conceptos",
        "code": "leccion_01",
        "title": "Conceptos de Estadística",
        "subtitle": "Población, muestra, variables y método científico",
        "apunte": "Lección 1 · Introducción a la estadística",
        "concepts": [
            ("Población", "Conjunto de TODAS las mediciones posibles de los individuos u objetos de interés que comparten una característica observable."),
            ("Muestra", "Subconjunto de datos recolectados de la población durante la investigación."),
            ("Unidad muestral", "El individuo u objeto concreto al que se le mide la característica."),
            ("Censo", "Medición de la variable en TODAS las unidades de la población."),
            ("Variable", "Característica de la población que puede tomar distintos valores. Se nota con mayúsculas (X, Y, Z)."),
            ("Cualitativa nominal", "Categorías sin orden: país, género, grupo sanguíneo."),
            ("Cualitativa ordinal", "Categorías con orden: escolaridad, intensidad de color."),
            ("Cuantitativa discreta", "Conteos, números enteros: atenciones de un cajero, casos covid."),
            ("Cuantitativa continua", "Cualquier valor en un intervalo real: peso, temperatura, pH, edad."),
            ("Parámetro", "Valor que resume a la POBLACIÓN. Se nota con letras griegas (μ, σ)."),
            ("Estadígrafo", "Función de los datos de la MUESTRA usada para estimar parámetros."),
        ],
        "theory": """
<p>La <b>Estadística</b> es la rama de la matemática que estudia la variabilidad y los
procesos aleatorios que la generan, siguiendo las leyes de la probabilidad. Su misión es
sustentar el método científico: <b>reunir</b>, <b>consolidar</b>, <b>representar</b> y
<b>concluir</b> a partir de los datos.</p>

<p>Se divide en dos grandes áreas:</p>
<ul>
  <li><b>Estadística descriptiva</b> — recolecta, organiza y presenta los datos de una
  muestra. Resume el patrón global (tablas y gráficos) y calcula estadígrafos de centro,
  dispersión y forma. <i>No</i> generaliza.</li>
  <li><b>Estadística inferencial</b> — a partir de la muestra, genera modelos que permiten
  estimar características de la población completa.</li>
</ul>

<p>El paso clave antes de cualquier análisis en R es <b>clasificar correctamente cada
variable</b>. En R esto se traduce en el <i>tipo</i> del vector: <code>factor</code> para
cualitativas, <code>integer</code> para discretas y <code>numeric</code> para continuas.
Clasificar mal una variable hace que R aplique el análisis equivocado.</p>
""",
        "examples": [
            {
                "title": "Tu primera sesión de R",
                "explain": "R funciona como una calculadora gigante. Asigna con <code>&lt;-</code> y consulta el tipo con <code>class()</code>.",
                "code": 'edad <- 27\nnombre <- "Camila"\ncat("Hola", nombre, "- edad:", edad, "\\n")\nclass(edad)\nclass(nombre)',
            },
            {
                "title": "Vectores: la unidad básica de datos",
                "explain": "Un vector guarda muchos valores del mismo tipo. Es la columna de una tabla.",
                "code": 'ventas <- c(120, 95, 130, 110, 88, 142)\nventas\nlength(ventas)\nsum(ventas)\nmean(ventas)',
            },
            {
                "title": "Variable cualitativa: el factor",
                "explain": "Las cualitativas se modelan con <code>factor()</code>. Para las ordinales usamos <code>ordered=TRUE</code> con los niveles en orden.",
                "code": 'genero <- factor(c("F","M","F","F","M"))\ntable(genero)\n\nescolaridad <- factor(c("Media","Superior","Basica","Superior"),\n  levels = c("Basica","Media","Superior"), ordered = TRUE)\nescolaridad\nescolaridad > "Media"',
            },
            {
                "title": "Población vs muestra (simulación)",
                "explain": "Creamos una población de 100.000 sueldos y extraemos una muestra de 50 con <code>sample()</code>. Observa cómo la media muestral se aproxima al parámetro.",
                "code": 'set.seed(2024)\npoblacion <- round(rnorm(100000, mean = 850, sd = 120))\nmu <- mean(poblacion)            # parametro\nmuestra <- sample(poblacion, 50)  # muestra\nxbar <- mean(muestra)            # estadigrafo\ncat("Parametro mu  =", round(mu,2), "\\n")\ncat("Estadigrafo x =", round(xbar,2), "\\n")',
            },
        ],
        "dataset": "iris",
        "exercises": [
            "Crea un vector con las notas de 8 alumnos y calcula su promedio y su máximo.",
            "Clasifica estas variables (nominal/ordinal/discreta/continua): color de auto, n° de hijos, temperatura, talla de polera (S/M/L).",
            "Extrae una muestra de 30 elementos de <code>poblacion</code> y compara su media con μ.",
        ],
    },

    # ============================================================ CAP 02
    {
        "num": 2,
        "slug": "frecuencias",
        "code": "leccion_02",
        "title": "Tablas de Frecuencia",
        "subtitle": "Datos agrupados, regla de Sturges y frecuencias",
        "apunte": "Lección 2 · Tablas de distribución de frecuencias",
        "concepts": [
            ("Datos no agrupados", "Registro crudo, sin orden ni clasificación."),
            ("Datos agrupados", "Datos organizados en clases o categorías."),
            ("Rango (R)", "R = x_max − x_min."),
            ("Regla de Sturges", "Número de clases: K = 1 + 3.3·log10(n). Debe quedar entre 5 y 15."),
            ("Amplitud (c)", "Ancho de cada clase: c = R / K."),
            ("Marca de clase (xi)", "Punto medio de la clase: (Li_inf + Li_sup)/2."),
            ("Frecuencia absoluta (ni)", "N° de datos que caen en la clase."),
            ("Frecuencia relativa (fi)", "fi = ni / n."),
            ("Frecuencia acumulada (Ni)", "Suma de las absolutas hasta esa clase."),
        ],
        "theory": """
<p>Cuando hay muchos datos continuos los <b>agrupamos en clases</b> para poder verlos. La
construcción de una tabla de distribución de frecuencias sigue la metodología del Apunte 2:</p>
<ol>
  <li>Hallar <b>x_min</b>, <b>x_max</b> y el rango <b>R = x_max − x_min</b>.</li>
  <li>Elegir el n° de clases con <b>Sturges</b>: <code>K = 1 + 3.3·log10(n)</code> (entre 5 y 15).</li>
  <li>Amplitud <b>c = R / K</b>, con la precisión de los datos.</li>
  <li>Construir los límites de clase y contar cuántos datos caen en cada una (<b>ni</b>).</li>
  <li>Calcular fi, fi%, Ni, Fi, Fi%.</li>
</ol>
<p>En R todo esto lo resuelve la familia <code>cut()</code> + <code>table()</code>, y
<code>hist()</code> incluso aplica una regla de clases automáticamente. Aprenderás a hacerlo
a mano (para entender) y de forma automática (para producir).</p>
""",
        "examples": [
            {
                "title": "Número de clases con Sturges",
                "explain": "Calculamos K para n datos. <code>nclass.Sturges()</code> es la función nativa de R.",
                "code": 'set.seed(1)\nventas <- round(runif(40, 50, 200))   # 40 vendedores\nn <- length(ventas)\nK <- ceiling(1 + 3.3 * log10(n))\ncat("n =", n, " -> K (Sturges) =", K, "\\n")\nnclass.Sturges(ventas)   # version nativa de R',
            },
            {
                "title": "Tabla de frecuencias automática",
                "explain": "<code>cut()</code> agrupa en intervalos y <code>table()</code> cuenta. Construimos todas las frecuencias en un data.frame.",
                "code": 'set.seed(1); ventas <- round(runif(40, 50, 200))\nclases <- cut(ventas, breaks = nclass.Sturges(ventas))\nni <- table(clases)\nfi <- prop.table(ni)\ntabla <- data.frame(\n  clase = names(ni),\n  ni    = as.integer(ni),\n  fi    = round(as.numeric(fi), 3),\n  fi_pct= round(as.numeric(fi)*100, 1),\n  Ni    = cumsum(as.integer(ni)),\n  Fi    = round(cumsum(as.numeric(fi)), 3)\n)\ntabla',
            },
            {
                "title": "Tabla para variable discreta / cualitativa",
                "explain": "Si la variable es discreta o categórica, la tabla sale directo con <code>table()</code>.",
                "code": 'defectos <- c(0,1,0,2,1,0,3,1,0,0,2,1,1,0,2)\ntab <- table(defectos)\ndata.frame(\n  valor = names(tab),\n  ni = as.integer(tab),\n  fi = round(prop.table(tab), 3),\n  Ni = cumsum(as.integer(tab))\n)',
            },
        ],
        "dataset": "airquality",
        "exercises": [
            "Genera 60 datos con <code>rnorm(60, 170, 8)</code> (estaturas) y construye su tabla de frecuencias con Sturges.",
            "¿Cuántas clases sugiere Sturges para n = 100? ¿Y para n = 1000? Verifica con R.",
            "Calcula la frecuencia relativa porcentual acumulada (Fi%) de la tabla de ventas.",
        ],
    },

    # ============================================================ CAP 03
    {
        "num": 3,
        "slug": "graficos",
        "code": "leccion_03",
        "title": "Representación Gráfica",
        "subtitle": "Barras, histograma, torta, boxplot y ojiva",
        "apunte": "Lección 3 · Estadística descriptiva, gráficos",
        "concepts": [
            ("Gráfico de barras", "Rectángulos separados para variables cualitativas/discretas."),
            ("Histograma", "Rectángulos contiguos para variables continuas agrupadas."),
            ("Polígono de frecuencias", "Une las marcas de clase con segmentos."),
            ("Ojiva", "Curva de frecuencias ACUMULADAS."),
            ("Gráfico circular", "Torta: proporciones del total."),
            ("Boxplot", "Caja con mediana, cuartiles y atípicos."),
            ("Elementos obligatorios", "Título, leyenda de ejes con nombre de variables y unidades."),
        ],
        "theory": """
<p>Un buen gráfico revela tendencias, estacionalidades, asociaciones y datos atípicos que
son difíciles de ver en una tabla. Según el Apunte 3, todo gráfico debe llevar
<b>título</b>, <b>nombres de los ejes</b> y <b>unidades de medida</b>.</p>
<p>La elección depende del tipo de variable:</p>
<ul>
  <li><b>Cualitativa</b> → barras o torta.</li>
  <li><b>Continua</b> → histograma, polígono u ojiva.</li>
  <li><b>Comparar grupos</b> → boxplot.</li>
</ul>
<p>R dibuja todo esto con funciones base: <code>barplot()</code>, <code>hist()</code>,
<code>pie()</code>, <code>boxplot()</code> y <code>plot()</code>. Cada gráfico que generes
aparecerá en el panel de la derecha de la consola.</p>
""",
        "examples": [
            {
                "title": "Gráfico de barras",
                "explain": "Frecuencia de defectos por turno. Usamos colores y etiquetas.",
                "code": 'turno <- c("Mañana","Tarde","Noche")\ndefectos <- c(23, 17, 31)\nbarplot(defectos, names.arg = turno,\n        col = c("#00ff9c","#22d3ee","#ff2e97"),\n        main = "Defectos por turno",\n        xlab = "Turno", ylab = "N° de defectos")',
            },
            {
                "title": "Histograma de una variable continua",
                "explain": "El histograma usa clases contiguas. <code>breaks</code> controla el n° de barras.",
                "code": 'set.seed(7)\npeso <- rnorm(200, mean = 72, sd = 9)\nhist(peso, breaks = "Sturges", col = "#00ff9c",\n     border = "#0a0e14",\n     main = "Distribución del peso (kg)",\n     xlab = "Peso (kg)", ylab = "Frecuencia")',
            },
            {
                "title": "Boxplot: comparar grupos",
                "explain": "El boxplot muestra mediana, cuartiles y atípicos. Ideal para comparar.",
                "code": 'boxplot(count ~ spray, data = InsectSprays,\n        col = "#22d3ee",\n        main = "Insectos por tipo de spray",\n        xlab = "Spray", ylab = "Conteo")',
            },
            {
                "title": "Torta y ojiva",
                "explain": "La torta muestra proporciones; la ojiva, frecuencias acumuladas.",
                "code": 'par(mfrow = c(1,2))\npie(c(40,25,20,15), labels = c("A","B","C","D"),\n    col = c("#00ff9c","#22d3ee","#ff2e97","#ffb627"),\n    main = "Participacion")\n\nset.seed(3); x <- rnorm(100, 50, 10)\nh <- hist(x, plot = FALSE)\nplot(h$mids, cumsum(h$counts), type = "o", col = "#00ff9c",\n     lwd = 2, main = "Ojiva", xlab = "x", ylab = "Frec. acumulada")\npar(mfrow = c(1,1))',
            },
        ],
        "dataset": "mtcars",
        "exercises": [
            "Dibuja un histograma de <code>mtcars$mpg</code> con 8 clases y título propio.",
            "Compara <code>mpg</code> según n° de cilindros con un boxplot: <code>boxplot(mpg ~ cyl, data = mtcars)</code>.",
            "Crea un gráfico de barras de la frecuencia de cilindros: <code>barplot(table(mtcars$cyl))</code>.",
        ],
    },

    # ============================================================ CAP 04
    {
        "num": 4,
        "slug": "posicion",
        "code": "leccion_04",
        "title": "Estadígrafos de Posición",
        "subtitle": "Media, mediana, moda, cuartiles y percentiles",
        "apunte": "Lección 4 · Estadígrafos de posición",
        "concepts": [
            ("Media aritmética", "Promedio: x̄ = Σxi / n. Es el centro de equilibrio."),
            ("Mediana", "Valor central que deja 50% bajo y 50% sobre él. Resistente a atípicos."),
            ("Moda", "Valor que más se repite."),
            ("Cuartiles", "Q1, Q2, Q3 dividen los datos en 4 partes iguales."),
            ("Percentiles", "Dividen en 100 partes. P50 = mediana."),
            ("Media ponderada", "Promedio que pesa cada valor por su importancia."),
        ],
        "theory": """
<p>Tras graficar, cuantificamos el <b>centro</b> de los datos. Los estadígrafos de posición
(o tendencia central) buscan un valor que represente a todo el conjunto.</p>
<ul>
  <li><b>Media</b> (<code>mean()</code>) — usa todos los datos, pero le afectan los atípicos.</li>
  <li><b>Mediana</b> (<code>median()</code>) — el valor central, robusto frente a atípicos.</li>
  <li><b>Moda</b> — R no trae función nativa; se obtiene con <code>table()</code>.</li>
  <li><b>Cuartiles / percentiles</b> (<code>quantile()</code>) — posición relativa.</li>
</ul>
<p>Regla práctica: si media ≈ mediana, la distribución es simétrica. Si media &gt; mediana,
hay asimetría a la derecha (cola de valores altos).</p>
""",
        "examples": [
            {
                "title": "Media, mediana y cuartiles",
                "explain": "<code>summary()</code> entrega de un golpe mínimo, cuartiles, media y máximo.",
                "code": 'sueldos <- c(620, 680, 700, 720, 750, 800, 950, 3200)\nmean(sueldos)\nmedian(sueldos)\nquantile(sueldos)\nsummary(sueldos)',
            },
            {
                "title": "La moda (función propia)",
                "explain": "Como R no tiene <code>mode()</code> estadística, la definimos nosotros.",
                "code": 'moda <- function(x){\n  t <- table(x)\n  as.numeric(names(t)[t == max(t)])\n}\ndatos <- c(2,3,3,4,4,4,5,6,4,3)\nmoda(datos)',
            },
            {
                "title": "Por qué la mediana resiste atípicos",
                "explain": "Cambiamos un valor por uno enorme: la media se dispara, la mediana casi no se mueve.",
                "code": 'x <- c(10,12,13,14,15)\ncat("Media:", mean(x), " Mediana:", median(x), "\\n")\nx[5] <- 900   # un atipico\ncat("Media:", mean(x), " Mediana:", median(x), "\\n")',
            },
            {
                "title": "Percentiles personalizados",
                "explain": "<code>quantile()</code> con <code>probs</code> calcula cualquier percentil.",
                "code": 'set.seed(2); notas <- round(rnorm(120, 5.2, 0.8), 1)\nquantile(notas, probs = c(0.10, 0.25, 0.50, 0.90))',
            },
        ],
        "dataset": "ToothGrowth",
        "exercises": [
            "Calcula media, mediana y los 3 cuartiles de <code>mtcars$hp</code>.",
            "Usa la función <code>moda()</code> sobre <code>mtcars$cyl</code>.",
            "Encuentra el percentil 95 de <code>rnorm(1000, 100, 15)</code>.",
        ],
    },

    # ============================================================ CAP 05
    {
        "num": 5,
        "slug": "dispersion",
        "code": "leccion_05",
        "title": "Dispersión, Asimetría y Curtosis",
        "subtitle": "Rango, varianza, desviación, CV y forma",
        "apunte": "Lección 5 · Estadígrafos de dispersión, asimetría y curtosis",
        "concepts": [
            ("Rango", "R = máximo − mínimo. Sensible a atípicos."),
            ("Varianza (s²)", "Promedio de las desviaciones al cuadrado respecto a la media."),
            ("Desviación estándar (s)", "Raíz de la varianza; en las mismas unidades que los datos."),
            ("Coef. de variación (CV)", "CV = s / x̄ · 100%. Dispersión relativa, sin unidades."),
            ("Asimetría (skewness)", "Mide si la distribución se inclina a un lado."),
            ("Curtosis", "Mide el apuntamiento respecto a la normal."),
        ],
        "theory": """
<p>El centro no basta: dos grupos con la misma media pueden ser muy distintos. Los
<b>estadígrafos de dispersión</b> miden la variabilidad respecto al centro.</p>
<ul>
  <li><b>Varianza</b> (<code>var()</code>) y <b>desviación estándar</b> (<code>sd()</code>).</li>
  <li><b>Coeficiente de variación</b> — permite comparar dispersión entre variables con
  distintas unidades o escalas. Útil cuando comparas, por ejemplo, sueldos vs estaturas.</li>
</ul>
<p>La <b>forma</b> se mide con:</p>
<ul>
  <li><b>Asimetría</b> &gt; 0 → cola a la derecha; &lt; 0 → cola a la izquierda; ≈ 0 → simétrica.</li>
  <li><b>Curtosis</b> &gt; 3 → más apuntada que la normal (leptocúrtica); &lt; 3 → más plana.</li>
</ul>
""",
        "examples": [
            {
                "title": "Dispersión completa",
                "explain": "Rango, varianza, desviación y CV de un set de datos.",
                "code": 'x <- c(45, 52, 48, 61, 55, 49, 70, 53)\nrango <- max(x) - min(x)\ncv <- sd(x) / mean(x) * 100\ncat("Rango :", rango, "\\n")\ncat("Var   :", round(var(x),2), "\\n")\ncat("SD    :", round(sd(x),2), "\\n")\ncat("CV    :", round(cv,1), "%\\n")',
            },
            {
                "title": "Comparar dispersión con CV",
                "explain": "El CV permite comparar variabilidad entre variables de distinta escala.",
                "code": 'sueldos   <- c(600,650,700,900,1200)\nestaturas <- c(165,170,168,172,169)\ncv <- function(v) sd(v)/mean(v)*100\ncat("CV sueldos  :", round(cv(sueldos),1), "%\\n")\ncat("CV estaturas:", round(cv(estaturas),1), "%\\n")',
            },
            {
                "title": "Asimetría y curtosis (sin paquetes)",
                "explain": "Las definimos a mano con los momentos, tal como en la teoría.",
                "code": 'asimetria <- function(x){\n  n <- length(x); m <- mean(x); s <- sd(x)\n  sum((x-m)^3)/n / s^3\n}\ncurtosis <- function(x){\n  n <- length(x); m <- mean(x); s <- sd(x)\n  sum((x-m)^4)/n / s^4\n}\nset.seed(5); d <- rexp(500)        # exponencial: cola derecha\ncat("Asimetria:", round(asimetria(d),3), "\\n")\ncat("Curtosis :", round(curtosis(d),3), "\\n")',
            },
            {
                "title": "Visualizar la forma",
                "explain": "Comparamos una distribución simétrica y una asimétrica con histogramas.",
                "code": 'par(mfrow = c(1,2))\nset.seed(1)\nhist(rnorm(1000), col="#22d3ee", main="Simetrica", xlab="x")\nhist(rexp(1000),  col="#ff2e97", main="Asimetrica (+)", xlab="x")\npar(mfrow = c(1,1))',
            },
        ],
        "dataset": "mtcars",
        "exercises": [
            "Calcula el CV de <code>mtcars$mpg</code> y de <code>mtcars$hp</code>. ¿Cuál varía más?",
            "Obtén la desviación estándar de <code>airquality$Temp</code> (omite NA con <code>na.rm=TRUE</code>).",
            "Mide la asimetría de <code>mtcars$wt</code> con la función creada.",
        ],
    },

    # ============================================================ CAP 06
    {
        "num": 6,
        "slug": "bivariados",
        "code": "leccion_06",
        "title": "Datos Bivariados",
        "subtitle": "Covarianza, correlación y regresión lineal",
        "apunte": "Lección 6 · Datos bivariados",
        "concepts": [
            ("Datos bivariados", "Se registran DOS variables por individuo para ver si se relacionan."),
            ("Covarianza (Sxy)", "Variabilidad conjunta. >0 relación directa, <0 inversa."),
            ("Correlación de Pearson (r)", "Covarianza estandarizada, entre −1 y 1. Mide fuerza y sentido."),
            ("Diagrama de dispersión", "Nube de puntos (X, Y) para ver el patrón."),
            ("Regresión lineal", "Recta ŷ = a + b·x que mejor predice Y a partir de X."),
            ("R² (determinación)", "Proporción de la variación de Y explicada por X."),
        ],
        "theory": """
<p>Hasta ahora analizamos UNA variable. Con <b>datos bivariados</b> estudiamos la relación
entre DOS variables numéricas (X, Y).</p>
<ul>
  <li><b>Covarianza</b> (<code>cov()</code>) — signo de la relación, pero depende de las unidades.</li>
  <li><b>Correlación de Pearson</b> (<code>cor()</code>) — entre −1 y 1, no depende de unidades:
    <br>|r| cercano a 1 → relación fuerte; cercano a 0 → débil.</li>
</ul>
<p>Si hay relación lineal, ajustamos una <b>recta de regresión</b> con <code>lm()</code>
(linear model). Con ella podemos <b>predecir</b>. El <b>R²</b> indica qué tan bien la recta
explica los datos.</p>
""",
        "examples": [
            {
                "title": "Covarianza y correlación",
                "explain": "Relación entre horas de estudio y nota obtenida.",
                "code": 'horas <- c(2, 3, 5, 1, 6, 4, 7, 3)\nnota  <- c(3.5, 4.0, 5.5, 3.0, 6.2, 4.8, 6.5, 4.1)\ncov(horas, nota)\ncor(horas, nota)            # Pearson\ncor(horas, nota)^2          # R cuadrado',
            },
            {
                "title": "Diagrama de dispersión",
                "explain": "La nube de puntos muestra el patrón antes de modelar.",
                "code": 'horas <- c(2,3,5,1,6,4,7,3)\nnota  <- c(3.5,4.0,5.5,3.0,6.2,4.8,6.5,4.1)\nplot(horas, nota, pch = 19, col = "#00ff9c", cex = 1.5,\n     main = "Horas de estudio vs Nota",\n     xlab = "Horas", ylab = "Nota")\ngrid()',
            },
            {
                "title": "Regresión lineal con lm()",
                "explain": "Ajustamos ŷ = a + b·x y dibujamos la recta sobre los puntos.",
                "code": 'horas <- c(2,3,5,1,6,4,7,3)\nnota  <- c(3.5,4.0,5.5,3.0,6.2,4.8,6.5,4.1)\nmodelo <- lm(nota ~ horas)\ncoef(modelo)                 # intercepto y pendiente\nplot(horas, nota, pch=19, col="#22d3ee", cex=1.5,\n     main="Regresion lineal", xlab="Horas", ylab="Nota")\nabline(modelo, col="#ff2e97", lwd=2)',
            },
            {
                "title": "Predecir con el modelo",
                "explain": "Con <code>predict()</code> estimamos la nota para nuevas horas de estudio.",
                "code": 'horas <- c(2,3,5,1,6,4,7,3)\nnota  <- c(3.5,4.0,5.5,3.0,6.2,4.8,6.5,4.1)\nmodelo <- lm(nota ~ horas)\nnuevos <- data.frame(horas = c(4.5, 8))\npredict(modelo, nuevos)\nsummary(modelo)$r.squared',
            },
        ],
        "dataset": "cars",
        "exercises": [
            "Calcula la correlación entre <code>mtcars$wt</code> y <code>mtcars$mpg</code>. ¿Qué signo tiene?",
            "Ajusta <code>lm(mpg ~ wt, data = mtcars)</code> y dibuja la recta con <code>abline()</code>.",
            "Con el dataset <code>cars</code>, predice la distancia de frenado para una velocidad de 25.",
        ],
    },
]
