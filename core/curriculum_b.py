# -*- coding: utf-8 -*-
"""Contenido educativo de los Apuntes 7 a 11."""

CHAPTERS_B = [
    # ============================================================ CAP 07
    {
        "num": 7,
        "slug": "probabilidades",
        "code": "apunte_07",
        "title": "Probabilidades",
        "subtitle": "Espacios muestrales, eventos y axiomas",
        "apunte": "Apunte 7 · Probabilidades",
        "concepts": [
            ("Experimento aleatorio", "Produce resultados distintos aunque se repita igual."),
            ("Espacio muestral (Ω)", "Conjunto de TODOS los resultados posibles."),
            ("Evento", "Subconjunto del espacio muestral."),
            ("Con/sin reemplazo", "Si devolvemos o no el elemento extraído antes del siguiente."),
            ("Axiomas de Kolmogórov", "0 ≤ P(A) ≤ 1; P(Ω)=1; P(A∪B)=P(A)+P(B) si son disjuntos."),
            ("Regla de Laplace", "P(A) = casos favorables / casos posibles (equiprobables)."),
            ("Combinatoria", "Permutaciones y combinaciones para contar casos."),
        ],
        "theory": """
<p>Si repetimos un experimento bajo las mismas condiciones y obtenemos resultados distintos,
estamos ante el <b>azar</b>. Kolmogórov formalizó la probabilidad con axiomas.</p>
<ul>
  <li><b>Espacio muestral Ω</b> — todos los resultados posibles.</li>
  <li><b>Evento</b> — un subconjunto de Ω.</li>
  <li><b>Regla de Laplace</b> — para casos equiprobables: favorables / posibles.</li>
</ul>
<p>R es ideal para probabilidad porque puede <b>simular</b> miles de experimentos
(<code>sample()</code>, <code>replicate()</code>) y verificar la teoría con la
<i>ley de los grandes números</i>: al repetir mucho, la frecuencia relativa converge a la
probabilidad teórica. También calcula combinatoria con <code>choose()</code> y
<code>factorial()</code>.</p>
""",
        "examples": [
            {
                "title": "Simular el lanzamiento de un dado",
                "explain": "Simulamos 10.000 lanzamientos y comparamos con la probabilidad teórica 1/6.",
                "code": 'set.seed(14256)\ndado <- sample(1:6, 10000, replace = TRUE)\ntable(dado)\nprop.table(table(dado))   # se acercan a 0.1667',
            },
            {
                "title": "Regla de Laplace: suma de dos dados",
                "explain": "Espacio muestral de 36 resultados. ¿P(suma = 7)?",
                "code": 'espacio <- expand.grid(d1 = 1:6, d2 = 1:6)\nespacio$suma <- espacio$d1 + espacio$d2\nfavorables <- sum(espacio$suma == 7)\ncat("P(suma=7) =", favorables, "/ 36 =",\n    round(favorables/36, 4), "\\n")\ntable(espacio$suma)',
            },
            {
                "title": "Combinatoria",
                "explain": "Combinaciones y permutaciones con <code>choose()</code> y <code>factorial()</code>.",
                "code": '# De cuantas formas elijo 3 de 10 (sin orden)\nchoose(10, 3)\n# Permutaciones de 5 elementos\nfactorial(5)\n# Probabilidad de un Kino simple (6 de 25)\n1 / choose(25, 6)',
            },
            {
                "title": "Ley de los grandes números",
                "explain": "La frecuencia relativa de cara converge a 0.5 al aumentar los lanzamientos.",
                "code": 'set.seed(1)\nn <- 2000\nlanz <- sample(c("C","S"), n, replace = TRUE)\nfreq <- cumsum(lanz == "C") / (1:n)\nplot(freq, type = "l", col = "#00ff9c", lwd = 2,\n     ylim = c(0,1), main = "Ley de los grandes numeros",\n     xlab = "N° de lanzamientos", ylab = "Frec. de cara")\nabline(h = 0.5, col = "#ff2e97", lty = 2)',
            },
        ],
        "dataset": "HairEyeColor",
        "exercises": [
            "Simula 5000 lanzamientos de una moneda y calcula la proporción de caras.",
            "¿Cuál es P(suma = 11) al lanzar dos dados? Verifica con simulación y con Laplace.",
            "Calcula <code>choose(49, 6)</code>: combinaciones del Loto.",
        ],
    },

    # ============================================================ CAP 08
    {
        "num": 8,
        "slug": "condicional",
        "code": "apunte_08",
        "title": "Probabilidad Condicional",
        "subtitle": "Teorema de la probabilidad total y de Bayes",
        "apunte": "Apunte 8 · Probabilidad condicional",
        "concepts": [
            ("Probabilidad condicional", "P(A|B) = P(A∩B) / P(B), con P(B) ≠ 0."),
            ("Independencia", "A y B son independientes si P(A|B) = P(A)."),
            ("Probabilidad total", "P(A) = Σ P(A|Bi)·P(Bi) sobre una partición."),
            ("Teorema de Bayes", "P(Bi|A) = P(A|Bi)·P(Bi) / P(A). Invierte la condición."),
            ("Diagrama de árbol", "Representa las ramas de eventos sucesivos."),
        ],
        "theory": """
<p>Muchas veces la probabilidad de un evento <b>depende</b> de que otro haya ocurrido. Eso es
la <b>probabilidad condicional</b> P(A|B): "probabilidad de A dado B".</p>
<p>Dos teoremas clave:</p>
<ul>
  <li><b>Probabilidad total</b> — descompone P(A) según una partición de causas Bi.</li>
  <li><b>Teorema de Bayes</b> — <i>invierte</i> la condición: a partir de P(A|B) obtiene
  P(B|A). Es la base del razonamiento diagnóstico (tests médicos, control de calidad,
  filtros de spam).</li>
</ul>
<p>R no necesita paquetes para esto: se resuelve con aritmética y, sobre todo, se puede
<b>verificar por simulación</b>, que es la forma más intuitiva de convencerse de los
resultados (a veces contraintuitivos) de Bayes.</p>
""",
        "examples": [
            {
                "title": "Probabilidad condicional desde una tabla",
                "explain": "Con una tabla de contingencia calculamos P(A|B) directamente.",
                "code": '# Filas: defecto (Si/No) ; Columnas: maquina (M1/M2)\ntab <- matrix(c(8, 2, 5, 85), nrow = 2, byrow = TRUE,\n              dimnames = list(c("Defecto","OK"), c("M1","M2")))\ntab\n# P(Defecto | M1)\ntab["Defecto","M1"] / sum(tab[, "M1"])',
            },
            {
                "title": "Teorema de la probabilidad total",
                "explain": "Dos proveedores aportan piezas con distinta tasa de falla.",
                "code": 'P_B <- c(prov1 = 0.6, prov2 = 0.4)      # mezcla\nP_falla_dado_B <- c(prov1 = 0.02, prov2 = 0.05)\nP_falla <- sum(P_falla_dado_B * P_B)\ncat("P(falla) =", round(P_falla, 4), "\\n")',
            },
            {
                "title": "Teorema de Bayes",
                "explain": "Test médico: sensibilidad 99%, falsos positivos 5%, prevalencia 1%. ¿P(enfermo | test +)?",
                "code": 'prev   <- 0.01      # P(enfermo)\nsens   <- 0.99      # P(+ | enfermo)\nfpr    <- 0.05      # P(+ | sano)\nP_pos  <- sens*prev + fpr*(1-prev)          # prob. total\nP_enf_pos <- sens*prev / P_pos              # Bayes\ncat("P(enfermo | test+) =", round(P_enf_pos, 4), "\\n")',
            },
            {
                "title": "Verificar Bayes por simulación",
                "explain": "Simulamos 100.000 personas y contamos: la frecuencia confirma el cálculo.",
                "code": 'set.seed(8)\nN <- 100000\nenfermo <- runif(N) < 0.01\ntest <- ifelse(enfermo, runif(N) < 0.99, runif(N) < 0.05)\nmean(enfermo[test])   # P(enfermo | test+) empirico',
            },
        ],
        "dataset": "Titanic",
        "exercises": [
            "Con la matriz <code>tab</code>, calcula P(Defecto | M2).",
            "Si la prevalencia sube a 10%, recalcula P(enfermo | test+) con Bayes. ¿Cambia mucho?",
            "Simula el problema de Monty Hall y estima la probabilidad de ganar cambiando de puerta.",
        ],
    },

    # ============================================================ CAP 09
    {
        "num": 9,
        "slug": "va-discretas",
        "code": "apunte_09",
        "title": "Variables Aleatorias Discretas",
        "subtitle": "Función de cuantía, binomial y Poisson",
        "apunte": "Apunte 9 · Variables aleatorias discretas",
        "concepts": [
            ("Variable aleatoria", "Función que asigna un número a cada resultado del experimento."),
            ("Función de cuantía", "P(X = x): probabilidad de cada valor. Suma 1."),
            ("Valor esperado E(X)", "Media teórica: Σ x·P(x)."),
            ("Varianza V(X)", "Σ (x−E(X))²·P(x)."),
            ("Binomial", "n ensayos independientes, prob. p de éxito. dbinom/pbinom."),
            ("Poisson", "N° de eventos en un intervalo, tasa λ. dpois/ppois."),
        ],
        "theory": """
<p>Una <b>variable aleatoria discreta</b> toma valores aislados (0,1,2,…). Su comportamiento
se describe con la <b>función de cuantía</b> P(X = x).</p>
<p>R trae las distribuciones más usadas con un patrón de 4 funciones por distribución:</p>
<ul>
  <li><code>d…</code> → P(X = x) (cuantía)</li>
  <li><code>p…</code> → P(X ≤ x) (acumulada)</li>
  <li><code>q…</code> → cuantil (inversa)</li>
  <li><code>r…</code> → genera datos aleatorios</li>
</ul>
<p>Las dos estrella del apunte son <b>Binomial</b> (<code>dbinom</code>) y <b>Poisson</b>
(<code>dpois</code>).</p>
""",
        "examples": [
            {
                "title": "Distribución binomial",
                "explain": "Una máquina produce 8% de defectos. En un lote de 20, ¿P(exactamente 3 defectos)?",
                "code": 'n <- 20; p <- 0.08\ndbinom(3, n, p)              # P(X = 3)\npbinom(3, n, p)             # P(X <= 3)\n1 - pbinom(2, n, p)         # P(X >= 3)\nc(esperado = n*p, var = n*p*(1-p))',
            },
            {
                "title": "Graficar la función de cuantía",
                "explain": "Dibujamos P(X = x) para la binomial completa.",
                "code": 'n <- 20; p <- 0.08\nx <- 0:n\nplot(x, dbinom(x, n, p), type = "h", lwd = 3, col = "#00ff9c",\n     main = "Binomial(20, 0.08)", xlab = "x", ylab = "P(X=x)")\npoints(x, dbinom(x, n, p), pch = 19, col = "#ff2e97")',
            },
            {
                "title": "Distribución de Poisson",
                "explain": "Llegan en promedio 4 clientes por minuto. ¿P(exactamente 6)? ¿P(más de 5)?",
                "code": 'lambda <- 4\ndpois(6, lambda)            # P(X = 6)\nppois(5, lambda)            # P(X <= 5)\n1 - ppois(5, lambda)        # P(X > 5)',
            },
            {
                "title": "Esperanza y varianza empíricas",
                "explain": "Simulamos y comparamos con los valores teóricos n·p y n·p·(1−p).",
                "code": 'set.seed(9)\nsim <- rbinom(10000, size = 20, prob = 0.08)\ncat("E(X) teorico:", 20*0.08, " | empirico:", mean(sim), "\\n")\ncat("V(X) teorico:", 20*0.08*0.92, " | empirico:", round(var(sim),3), "\\n")',
            },
        ],
        "dataset": "warpbreaks",
        "exercises": [
            "Una moneda se lanza 10 veces. Calcula P(exactamente 7 caras) con <code>dbinom</code>.",
            "Si llegan 3 correos/hora (Poisson), ¿P(0 correos en una hora)?",
            "Grafica la cuantía de una Poisson con λ = 7 para x de 0 a 20.",
        ],
    },

    # ============================================================ CAP 10
    {
        "num": 10,
        "slug": "va-continuas",
        "code": "apunte_10",
        "title": "Variables Aleatorias Continuas",
        "subtitle": "Densidad, distribución normal y exponencial",
        "apunte": "Apunte 10 · Variables aleatorias continuas",
        "concepts": [
            ("Función de densidad f(x)", "Curva cuya área bajo ella vale 1. La probabilidad es área."),
            ("P(a ≤ X ≤ b)", "Área bajo f(x) entre a y b. P(X = x) = 0 en continuas."),
            ("Distribución Normal", "Campana simétrica N(μ, σ). dnorm/pnorm/qnorm."),
            ("Estandarización (Z)", "Z = (X − μ) / σ lleva a la normal estándar N(0,1)."),
            ("Exponencial", "Modela tiempos de espera. dexp/pexp."),
            ("Regla 68-95-99.7", "% de datos a 1, 2 y 3 desviaciones de la media."),
        ],
        "theory": """
<p>En una <b>variable continua</b> la probabilidad es el <b>área bajo la curva</b> de la
función de densidad f(x). Por eso P(X = x) = 0 y solo tienen sentido los intervalos.</p>
<p>La reina es la <b>distribución Normal</b> N(μ, σ):</p>
<ul>
  <li><code>dnorm(x, μ, σ)</code> → altura de la densidad.</li>
  <li><code>pnorm(x, μ, σ)</code> → P(X ≤ x) (área a la izquierda).</li>
  <li><code>qnorm(p, μ, σ)</code> → el valor que deja área p a la izquierda.</li>
  <li><code>rnorm(n, μ, σ)</code> → genera datos normales.</li>
</ul>
<p>La <b>estandarización</b> Z convierte cualquier normal en N(0,1), lo que conecta con la
tabla Z clásica del curso.</p>
""",
        "examples": [
            {
                "title": "Probabilidades con la normal",
                "explain": "Pesos N(72, 9). ¿P(X < 80)? ¿P(70 < X < 75)?",
                "code": 'mu <- 72; sigma <- 9\npnorm(80, mu, sigma)                       # P(X < 80)\npnorm(75, mu, sigma) - pnorm(70, mu, sigma) # P(70<X<75)\nqnorm(0.95, mu, sigma)                     # percentil 95',
            },
            {
                "title": "Dibujar la campana y sombrear un área",
                "explain": "Visualizamos P(X ≤ 80) como el área sombreada bajo la curva.",
                "code": 'mu <- 72; sigma <- 9\nx <- seq(mu-4*sigma, mu+4*sigma, length = 400)\nplot(x, dnorm(x, mu, sigma), type = "l", lwd = 2, col = "#22d3ee",\n     main = "Normal(72, 9)", xlab = "x", ylab = "f(x)")\nxs <- x[x <= 80]\npolygon(c(xs, 80), c(dnorm(xs, mu, sigma), 0), col = "#00ff9c80", border = NA)',
            },
            {
                "title": "Estandarización (puntaje Z)",
                "explain": "Convertimos a Z y verificamos que pnorm coincide.",
                "code": 'x <- 80; mu <- 72; sigma <- 9\nz <- (x - mu) / sigma\nz\npnorm(z)              # usando Z (N(0,1))\npnorm(x, mu, sigma)   # directo: mismo resultado',
            },
            {
                "title": "Regla 68-95-99.7 y exponencial",
                "explain": "Comprobamos la regla empírica y modelamos un tiempo de espera.",
                "code": 'set.seed(10)\nd <- rnorm(100000, 0, 1)\ncat("±1 sd:", round(mean(abs(d) < 1)*100,1), "%\\n")\ncat("±2 sd:", round(mean(abs(d) < 2)*100,1), "%\\n")\ncat("±3 sd:", round(mean(abs(d) < 3)*100,1), "%\\n")\n# Exponencial: P(espera < 2 min) con tasa 1/3\npexp(2, rate = 1/3)',
            },
        ],
        "dataset": "faithful",
        "exercises": [
            "Para N(500, 50), calcula P(X > 600) con <code>pnorm</code>.",
            "Encuentra el percentil 90 de una N(170, 8) (estaturas).",
            "Dibuja la densidad de una exponencial con tasa 0.5 entre 0 y 10.",
        ],
    },

    # ============================================================ CAP 11
    {
        "num": 11,
        "slug": "intervalos",
        "code": "apunte_11",
        "title": "Intervalos de Confianza",
        "subtitle": "Estimación de la media y la varianza",
        "apunte": "Apunte 11 · Intervalos de confianza",
        "concepts": [
            ("Inferencia estadística", "Generalizar de la muestra a la población."),
            ("Estimador insesgado", "Su valor esperado coincide con el parámetro (x̄ estima μ)."),
            ("Nivel de confianza", "1 − α (ej. 95%). α es el nivel de significación."),
            ("Intervalo de confianza", "Rango que con confianza 1−α contiene el parámetro."),
            ("IC para la media (σ conocida)", "x̄ ± z·σ/√n."),
            ("IC para la media (σ desconocida)", "x̄ ± t·s/√n (distribución t de Student)."),
            ("Margen de error", "La mitad del ancho del intervalo."),
        ],
        "theory": """
<p>La <b>inferencia</b> generaliza de la muestra a la población. Un <b>intervalo de
confianza</b> es un par de números que, con confianza 1−α, contiene el parámetro
desconocido (μ o σ²).</p>
<p>Compromiso clave: a mayor confianza, intervalo más ancho; a mayor n, intervalo más
angosto.</p>
<ul>
  <li><b>σ conocida</b> → usar z: <code>qnorm()</code>.</li>
  <li><b>σ desconocida</b> (lo habitual) → usar t de Student: <code>qt()</code>. R lo
  resuelve completo con <code>t.test()</code>.</li>
</ul>
""",
        "examples": [
            {
                "title": "IC para la media con t.test()",
                "explain": "La forma directa: <code>t.test()</code> entrega el intervalo del 95%.",
                "code": 'set.seed(11)\nmuestra <- rnorm(30, mean = 850, sd = 120)\nt.test(muestra, conf.level = 0.95)',
            },
            {
                "title": "IC para la media paso a paso (σ desconocida)",
                "explain": "Construimos x̄ ± t·s/√n a mano para entender la fórmula.",
                "code": 'set.seed(11); x <- rnorm(30, 850, 120)\nn <- length(x); xbar <- mean(x); s <- sd(x)\nalpha <- 0.05\ntc <- qt(1 - alpha/2, df = n - 1)\nerror <- tc * s / sqrt(n)\nc(inferior = xbar - error, media = xbar, superior = xbar + error)',
            },
            {
                "title": "Efecto del nivel de confianza",
                "explain": "Comparamos el ancho del IC al 90%, 95% y 99%.",
                "code": 'set.seed(11); x <- rnorm(30, 850, 120)\nfor (conf in c(0.90, 0.95, 0.99)) {\n  ic <- t.test(x, conf.level = conf)$conf.int\n  cat("Conf", conf*100, "% -> [", round(ic[1],1), ",",\n      round(ic[2],1), "] ancho =", round(diff(ic),1), "\\n")\n}',
            },
            {
                "title": "Tamaño muestral y precisión",
                "explain": "A mayor n, el intervalo se angosta. Lo verificamos visualmente.",
                "code": 'set.seed(1)\nanchos <- sapply(c(10,30,60,120,300), function(n){\n  x <- rnorm(n, 850, 120)\n  diff(t.test(x)$conf.int)\n})\nplot(c(10,30,60,120,300), anchos, type = "o", pch = 19,\n     col = "#00ff9c", lwd = 2,\n     main = "Ancho del IC vs tamano muestral",\n     xlab = "n", ylab = "Ancho del intervalo")',
            },
        ],
        "dataset": "sleep",
        "exercises": [
            "Construye el IC del 99% para <code>mtcars$mpg</code> con <code>t.test()</code>.",
            "Calcula a mano el margen de error de una muestra de n=50, s=15, al 95%.",
            "Genera 100 muestras de N(0,1) y cuenta cuántos IC del 95% contienen el 0.",
        ],
    },
]
