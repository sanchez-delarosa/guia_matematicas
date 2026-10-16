"""
Aplica notación LaTeX KaTeX a todos los 276 reactivos de guia_matematicas.
Garantiza que todas las preguntas y opciones de opción múltiple
se rendericen con tipografía matemática profesional en KaTeX.
"""

import json
from pathlib import Path

# Diccionario completo de reactivos normalizados con KaTeX
# Cada entrada contiene la pregunta y las 4 opciones formateadas en LaTeX
REACTIVOS_LATEX = {
    # =========================================================================
    # TEMA 1: Operaciones con números reales, complejos y expresiones algebraicas
    # =========================================================================
    "MOCK-0001": {
        "pregunta": "La temperatura cambia de $-7^\\circ\\text{C}$ a $12^\\circ\\text{C}$. ¿Cuál es la diferencia?",
        "respuestas": {"A": "$5^\\circ\\text{C}$", "B": "$19^\\circ\\text{C}$", "C": "$-19^\\circ\\text{C}$", "D": "$-5^\\circ\\text{C}$"}
    },
    "MOCK-0002": {
        "pregunta": "Calcula: $-8.4 + 3.7 - 1.6$.",
        "respuestas": {"A": "$-6.3$", "B": "$-3.1$", "C": "$6.3$", "D": "$-13.7$"}
    },
    "MOCK-0003": {
        "pregunta": "Un saldo de $-\\$125$ recibe un depósito de $\\$80$. ¿Cuál es el nuevo saldo?",
        "respuestas": {"A": "$-\\$205$", "B": "$-\\$45$", "C": "$\\$45$", "D": "$\\$205$"}
    },
    "MOCK-0004": {
        "pregunta": "Calcula: $\\left(\\frac{3}{5}\\right) \\div \\left(-\\frac{9}{10}\\right)$.",
        "respuestas": {"A": "$-\\frac{2}{3}$", "B": "$\\frac{2}{3}$", "C": "$-\\frac{3}{2}$", "D": "$\\frac{3}{2}$"}
    },
    "MOCK-0005": {
        "pregunta": "Un vehículo recorre $72\\text{ km}$ con $8\\text{ L}$. ¿Cuál es su rendimiento?",
        "respuestas": {"A": "$8\\text{ km/L}$", "B": "$9\\text{ km/L}$", "C": "$10\\text{ km/L}$", "D": "$12\\text{ km/L}$"}
    },
    "MOCK-0006": {
        "pregunta": "Calcula: $4\\left[2^{-1} + \\frac{3}{2}\\right]$.",
        "respuestas": {"A": "$4$", "B": "$6$", "C": "$8$", "D": "$10$"}
    },
    "MOCK-0007": {
        "pregunta": "Calcula: $27^{2/3}$.",
        "respuestas": {"A": "$3$", "B": "$6$", "C": "$9$", "D": "$18$"}
    },
    "MOCK-0008": {
        "pregunta": "Simplifica: $\\sqrt{\\frac{144}{25}}$.",
        "respuestas": {"A": "$\\frac{12}{5}$", "B": "$\\frac{5}{12}$", "C": "$\\frac{24}{5}$", "D": "$\\frac{6}{5}$"}
    },
    "MOCK-0009": {
        "pregunta": "El valor de $16^{-3/4}$ es:",
        "respuestas": {"A": "$\\frac{1}{4}$", "B": "$\\frac{1}{8}$", "C": "$\\frac{1}{16}$", "D": "$8$"}
    },
    "MOCK-0010": {
        "pregunta": "Calcula: $(3-2i) + (5+7i)$.",
        "respuestas": {"A": "$8+5i$", "B": "$2+9i$", "C": "$8+9i$", "D": "$2+5i$"}
    },
    "MOCK-0011": {
        "pregunta": "Calcula: $(4+6i) - (1-3i)$.",
        "respuestas": {"A": "$3+3i$", "B": "$3+9i$", "C": "$5+3i$", "D": "$5+9i$"}
    },
    "MOCK-0012": {
        "pregunta": "Simplifica: $2i - (3-5i) + 4$.",
        "respuestas": {"A": "$1+7i$", "B": "$7+i$", "C": "$1-3i$", "D": "$-7+7i$"}
    },
    "MOCK-0013": {
        "pregunta": "Calcula: $(2+3i)(1-2i)$.",
        "respuestas": {"A": "$8-i$", "B": "$-4-i$", "C": "$8+i$", "D": "$-4+i$"}
    },
    "MOCK-0014": {
        "pregunta": "Calcula: $(4-i)(4+i)$.",
        "respuestas": {"A": "$15$", "B": "$16$", "C": "$17$", "D": "$8$"}
    },
    "MOCK-0015": {
        "pregunta": "El producto $i(3-5i)$ es:",
        "respuestas": {"A": "$-5+3i$", "B": "$5+3i$", "C": "$3-5i$", "D": "$-3+5i$"}
    },
    "MOCK-0016": {
        "pregunta": "Simplifica: $(4x^2-3x+2) + (x^2+5x-7)$.",
        "respuestas": {"A": "$5x^2+2x-5$", "B": "$3x^2+2x-5$", "C": "$5x^2-8x+9$", "D": "$5x^2+8x-5$"}
    },
    "MOCK-0017": {
        "pregunta": "Simplifica: $(6a-2b) - (3a+5b)$.",
        "respuestas": {"A": "$3a+3b$", "B": "$9a-7b$", "C": "$3a-7b$", "D": "$3a+7b$"}
    },
    "MOCK-0018": {
        "pregunta": "Reduce: $2m^2-3m+4-m^2+8m-1$.",
        "respuestas": {"A": "$m^2+5m+3$", "B": "$3m^2+5m+3$", "C": "$m^2-11m+5$", "D": "$m^2+5m+5$"}
    },
    "MOCK-0019": {
        "pregunta": "Desarrolla: $(2x-3)(x+4)$.",
        "respuestas": {"A": "$2x^2+5x-12$", "B": "$2x^2+11x-12$", "C": "$2x^2-5x+12$", "D": "$2x^2+8x-3$"}
    },
    "MOCK-0020": {
        "pregunta": "Simplifica: $\\frac{12x^3y^2}{3xy}$.",
        "respuestas": {"A": "$4x^2y$", "B": "$4x^3y$", "C": "$9x^2y$", "D": "$4x^2y^2$"}
    },
    "MOCK-0021": {
        "pregunta": "El cociente $\\frac{x^2-9}{x-3}$, con $x \\neq 3$, es:",
        "respuestas": {"A": "$x-3$", "B": "$x+3$", "C": "$x^2+3$", "D": "$1$"}
    },
    "MOCK-0022": {
        "pregunta": "Simplifica: $(8x^6)^{1/3}$.",
        "respuestas": {"A": "$2x^2$", "B": "$4x^2$", "C": "$2x^3$", "D": "$8x^2$"}
    },
    "MOCK-0023": {
        "pregunta": "Simplifica: $(a^8)^{3/4}$, suponiendo $a > 0$.",
        "respuestas": {"A": "$a^6$", "B": "$a^5$", "C": "$a^{11}$", "D": "$a^2$"}
    },
    "MOCK-0024": {
        "pregunta": "La expresión $\\frac{x^{5/2}}{x^{1/2}}$, con $x > 0$, es:",
        "respuestas": {"A": "$x$", "B": "$x^2$", "C": "$x^3$", "D": "$x^{5/4}$"}
    },
    "MOCK-0025": {
        "pregunta": "Simplifica: $2\\sqrt{12} + \\sqrt{27}$.",
        "respuestas": {"A": "$5\\sqrt{3}$", "B": "$7\\sqrt{3}$", "C": "$6\\sqrt{3}$", "D": "$3\\sqrt{39}$"}
    },
    "MOCK-0026": {
        "pregunta": "Racionaliza: $\\frac{5}{\\sqrt{5}}$.",
        "respuestas": {"A": "$\\sqrt{5}$", "B": "$5\\sqrt{5}$", "C": "$\\frac{1}{\\sqrt{5}}$", "D": "$25$"}
    },
    "MOCK-0027": {
        "pregunta": "Calcula: $\\sqrt{8} \\cdot \\sqrt{18}$.",
        "respuestas": {"A": "$6$", "B": "$12$", "C": "$12\\sqrt{2}$", "D": "$24$"}
    },

    # =========================================================================
    # TEMA 2: Productos notables y factorización
    # =========================================================================
    "MOCK-0028": {
        "pregunta": "El término central de $(x+2)^2$ es:",
        "respuestas": {"A": "$2x$", "B": "$4x$", "C": "$4$", "D": "$x^2$"}
    },
    "MOCK-0029": {
        "pregunta": "Desarrolla: $(a-b)^3$.",
        "respuestas": {
            "A": "$a^3-3a^2b+3ab^2-b^3$",
            "B": "$a^3-3ab-b^3$",
            "C": "$a^3+3a^2b+3ab^2+b^3$",
            "D": "$a^3-b^3$"
        }
    },
    "MOCK-0030": {
        "pregunta": "El coeficiente de $x^2$ en $(x+1)^4$ es:",
        "respuestas": {"A": "$4$", "B": "$6$", "C": "$8$", "D": "$12$"}
    },
    "MOCK-0031": {
        "pregunta": "Si $P(x) = x^3-2x^2-5x+6$, ¿cuál es el residuo al dividir entre $x-1$?",
        "respuestas": {"A": "$0$", "B": "$1$", "C": "$-1$", "D": "$6$"}
    },
    "MOCK-0032": {
        "pregunta": "¿Cuál es factor de $P(x) = x^3+x^2-4x-4$?",
        "respuestas": {"A": "$x-1$", "B": "$x+1$", "C": "$x-2$", "D": "$x+4$"}
    },
    "MOCK-0033": {
        "pregunta": "Si al dividir $P(x)$ entre $x+3$ el residuo es $5$, entonces:",
        "respuestas": {"A": "$P(3)=5$", "B": "$P(-3)=5$", "C": "$P(5)=-3$", "D": "$P(-5)=3$"}
    },
    "MOCK-0034": {
        "pregunta": "Simplifica: $\\frac{x^2-4}{x+2}$, con $x \\neq -2$.",
        "respuestas": {"A": "$x+2$", "B": "$x-2$", "C": "$x^2-2$", "D": "$1$"}
    },
    "MOCK-0035": {
        "pregunta": "Simplifica: $\\frac{a^2-2a}{a}$, con $a \\neq 0$.",
        "respuestas": {"A": "$a-2$", "B": "$a^2-2$", "C": "$a+2$", "D": "$1-2a$"}
    },
    "MOCK-0036": {
        "pregunta": "Simplifica: $\\frac{y^2+5y+6}{y+2}$, con $y \\neq -2$.",
        "respuestas": {"A": "$y+2$", "B": "$y+3$", "C": "$y-3$", "D": "$y^2+3$"}
    },
    "MOCK-0037": {
        "pregunta": "Calcula: $\\frac{1}{x} + \\frac{2}{x}$.",
        "respuestas": {"A": "$\\frac{3}{x}$", "B": "$\\frac{3}{2x}$", "C": "$\\frac{2}{x^2}$", "D": "$3x$"}
    },
    "MOCK-0038": {
        "pregunta": "Calcula: $\\frac{1}{a} - \\frac{1}{b}$.",
        "respuestas": {"A": "$\\frac{a-b}{ab}$", "B": "$\\frac{b-a}{ab}$", "C": "$\\frac{1}{a-b}$", "D": "$\\frac{a+b}{ab}$"}
    },
    "MOCK-0039": {
        "pregunta": "Multiplica: $\\left[\\frac{x}{x+1}\\right] \\cdot \\left[\\frac{x+1}{3}\\right]$.",
        "respuestas": {"A": "$\\frac{x}{3}$", "B": "$\\frac{x+1}{3}$", "C": "$\\frac{x(x+1)}{3}$", "D": "$3x$"}
    },

    # =========================================================================
    # TEMA 3: Ecuaciones
    # =========================================================================
    "MOCK-0040": {
        "pregunta": "¿Cuál expresión es una identidad?",
        "respuestas": {"A": "$2x+1=7$", "B": "$(x+1)^2=x^2+2x+1$", "C": "$x-3>0$", "D": "$x^2=9$"}
    },
    "MOCK-0041": {
        "pregunta": "¿Cuál expresión es una ecuación?",
        "respuestas": {"A": "$3x-5=10$", "B": "$x+2<7$", "C": "$2(x+1)=2x+2$ para todo $x$", "D": "$x \\ge 0$"}
    },
    "MOCK-0042": {
        "pregunta": "Si $a=b$, ¿cuál operación conserva la igualdad?",
        "respuestas": {
            "A": "Sumar el mismo número a ambos miembros",
            "B": "Sumar números distintos",
            "C": "Multiplicar un miembro por cero solamente",
            "D": "Cambiar un signo en un miembro"
        }
    },
    "MOCK-0043": {
        "pregunta": "Resuelve: $4x-7=13$.",
        "respuestas": {"A": "$x=3$", "B": "$x=4$", "C": "$x=5$", "D": "$x=6$"}
    },
    "MOCK-0044": {
        "pregunta": "Resuelve: $\\frac{x}{3}+2=5$.",
        "respuestas": {"A": "$x=1$", "B": "$x=7$", "C": "$x=9$", "D": "$x=15$"}
    },
    "MOCK-0045": {
        "pregunta": "Resuelve: $2(x-3)=x+5$.",
        "respuestas": {"A": "$x=8$", "B": "$x=11$", "C": "$x=-1$", "D": "$x=5$"}
    },
    "MOCK-0046": {
        "pregunta": "Resuelve: $x^2-5x+6=0$.",
        "respuestas": {"A": "$x=1,\\, 6$", "B": "$x=2,\\, 3$", "C": "$x=-2,\\, -3$", "D": "$x=-1,\\, 6$"}
    },
    "MOCK-0047": {
        "pregunta": "Las raíces de $2x^2-8=0$ son:",
        "respuestas": {"A": "$\\pm 2$", "B": "$\\pm 4$", "C": "$2$ y $4$", "D": "$-2$ y $4$"}
    },
    "MOCK-0048": {
        "pregunta": "El discriminante de $x^2+4x+5=0$ es:",
        "respuestas": {"A": "$4$", "B": "$-4$", "C": "$16$", "D": "$36$"}
    },

    # =========================================================================
    # TEMA 4: Desigualdades
    # =========================================================================
    "MOCK-0049": {
        "pregunta": "Resuelve: $3x-4 \\le 8$.",
        "respuestas": {"A": "$x \\le 4$", "B": "$x \\ge 4$", "C": "$x < 12$", "D": "$x \\ge 12$"}
    },
    "MOCK-0050": {
        "pregunta": "Resuelve: $-2x > 6$.",
        "respuestas": {"A": "$x > -3$", "B": "$x < -3$", "C": "$x > 3$", "D": "$x < 3$"}
    },
    "MOCK-0051": {
        "pregunta": "El intervalo solución de $5 \\le x+2 < 9$ es:",
        "respuestas": {"A": "$[3, 7)$", "B": "$(3, 7]$", "C": "$[-3, 11)$", "D": "$[7, 11)$"}
    },

    # =========================================================================
    # TEMA 5: Sistemas de ecuaciones
    # =========================================================================
    "MOCK-0052": {
        "pregunta": "Resuelve: $x+y=7$, $x-y=1$.",
        "respuestas": {"A": "$x=3,\\, y=4$", "B": "$x=4,\\, y=3$", "C": "$x=6,\\, y=1$", "D": "$x=5,\\, y=2$"}
    },
    "MOCK-0053": {
        "pregunta": "Resuelve: $2x+y=8$, $x-y=1$.",
        "respuestas": {"A": "$x=2,\\, y=4$", "B": "$x=3,\\, y=2$", "C": "$x=4,\\, y=0$", "D": "$x=1,\\, y=6$"}
    },
    "MOCK-0054": {
        "pregunta": "Dos boletos y tres snacks cuestan $\\$190$; un boleto y un snack cuestan $\\$70$. ¿Precio del boleto?",
        "respuestas": {"A": "$\\$20$", "B": "$\\$40$", "C": "$\\$50$", "D": "$\\$60$"}
    },
    "MOCK-0055": {
        "pregunta": "Resuelve: $x+y+z=6$, $x-y=0$, $z=2$.",
        "respuestas": {"A": "$(2, 2, 2)$", "B": "$(1, 1, 4)$", "C": "$(3, 3, 0)$", "D": "$(2, 1, 3)$"}
    },
    "MOCK-0056": {
        "pregunta": "En el sistema $x+y+z=4$, $x+y-z=0$, $x-y=0$, el valor de $z$ es:",
        "respuestas": {"A": "$1$", "B": "$2$", "C": "$3$", "D": "$4$"}
    },
    "MOCK-0057": {
        "pregunta": "El determinante principal del sistema $x+y+z=1$, $2x-y+z=2$, $x+2y-z=3$ es:",
        "respuestas": {"A": "$-5$", "B": "$5$", "C": "$0$", "D": "$3$"}
    },

    # =========================================================================
    # TEMA 6: Funciones algebraicas
    # =========================================================================
    "MOCK-0058": {
        "pregunta": "El dominio de $f(x) = \\frac{1}{x-4}$ es:",
        "respuestas": {"A": "$\\mathbb{R}$", "B": "$\\mathbb{R} \\setminus \\{4\\}$", "C": "$(4, \\infty)$", "D": "$[-4, 4]$"}
    },
    "MOCK-0059": {
        "pregunta": "Si $f: \\{1,2,3\\} \\to \\mathbb{R}$ y $f(x) = 2x$, el dominio es:",
        "respuestas": {"A": "$\\{2, 4, 6\\}$", "B": "$\\mathbb{R}$", "C": "$\\{1, 2, 3\\}$", "D": "$\\{1, 2, 3, 4, 6\\}$"}
    },
    "MOCK-0060": {
        "pregunta": "El dominio de $f(x) = \\sqrt{x+5}$ es:",
        "respuestas": {"A": "$x > -5$", "B": "$x \\ge -5$", "C": "$x \\le -5$", "D": "$\\mathbb{R} \\setminus \\{-5\\}$"}
    },
    "MOCK-0061": {
        "pregunta": "El rango de $f(x) = x^2+2$ es:",
        "respuestas": {"A": "$[0, \\infty)$", "B": "$[2, \\infty)$", "C": "$(-\\infty, 2]$", "D": "$\\mathbb{R}$"}
    },
    "MOCK-0062": {
        "pregunta": "El rango de $f(x) = -x^2+4$ es:",
        "respuestas": {"A": "$[4, \\infty)$", "B": "$(-\\infty, 4]$", "C": "$[0, 4]$", "D": "$\\mathbb{R}$"}
    },
    "MOCK-0063": {
        "pregunta": "Si $f(x) = 3$ para todo $x$, su rango es:",
        "respuestas": {"A": "$\\mathbb{R}$", "B": "$\\{0, 3\\}$", "C": "$\\{3\\}$", "D": "$[3, \\infty)$"}
    },
    "MOCK-0064": {
        "pregunta": "¿Qué gráfica corresponde a $y = 2x+1$?",
        "respuestas": {
            "A": "Recta creciente con ordenada al origen 1",
            "B": "Recta decreciente con ordenada al origen 1",
            "C": "Parábola con vértice 1",
            "D": "Recta horizontal $y=1$"
        }
    },
    "MOCK-0065": {
        "pregunta": "La gráfica de $y = |x-2|$ tiene vértice en:",
        "respuestas": {"A": "$(0, 2)$", "B": "$(2, 0)$", "C": "$(-2, 0)$", "D": "$(0, -2)$"}
    },
    "MOCK-0066": {
        "pregunta": "La gráfica de $y = -(x+1)^2+3$ abre:",
        "respuestas": {"A": "A la derecha", "B": "A la izquierda", "C": "Hacia arriba", "D": "Hacia abajo"}
    },
    "MOCK-0067": {
        "pregunta": "¿Cuál relación está escrita en forma implícita?",
        "respuestas": {"A": "$y = 2x+3$", "B": "$y = \\sqrt{x}$", "C": "$x^2+xy+y^2=7$", "D": "$y = \\frac{1}{x}$"}
    },
    "MOCK-0068": {
        "pregunta": "Despeja $y$ de $3x+2y=8$.",
        "respuestas": {"A": "$y = \\frac{8-3x}{2}$", "B": "$y = 8 - \\frac{3x}{2}$", "C": "$y = \\frac{3x-8}{2}$", "D": "$y = 4 + \\frac{3x}{2}$"}
    },
    "MOCK-0069": {
        "pregunta": "La ecuación $x^2+y^2=9$ define $y$ explícitamente como:",
        "respuestas": {"A": "$y = 9-x^2$", "B": "$y = \\pm \\sqrt{9-x^2}$", "C": "$y = x^2-9$", "D": "$y = \\sqrt{x^2-9}$"}
    },
    "MOCK-0070": {
        "pregunta": "¿Cuál función es creciente en todo $\\mathbb{R}$?",
        "respuestas": {"A": "$f(x) = -2x$", "B": "$f(x) = x^3$", "C": "$f(x) = \\frac{1}{x}$", "D": "$f(x) = -x^2$"}
    },
    "MOCK-0071": {
        "pregunta": "La función $f(x) = -3x+1$ es:",
        "respuestas": {"A": "Creciente", "B": "Decreciente", "C": "Constante", "D": "Periódica"}
    },
    "MOCK-0072": {
        "pregunta": "En el intervalo $(0, \\infty)$, $f(x) = x^2$ es:",
        "respuestas": {"A": "Decreciente", "B": "Constante", "C": "Creciente", "D": "Discontinua"}
    },
    "MOCK-0073": {
        "pregunta": "¿En qué punto es discontinua $f(x) = \\frac{1}{x-2}$?",
        "respuestas": {"A": "$x = -2$", "B": "$x = 0$", "C": "$x = 1$", "D": "$x = 2$"}
    },
    "MOCK-0074": {
        "pregunta": "Para que $f(x) = \\begin{cases} x+1 & \\text{si } x<1 \\\\ k & \\text{si } x=1 \\\\ 3x-1 & \\text{si } x>1 \\end{cases}$ sea continua en $x=1$, $k$ debe ser:",
        "respuestas": {"A": "$0$", "B": "$1$", "C": "$2$", "D": "$3$"}
    },
    "MOCK-0075": {
        "pregunta": "¿Cuál función es continua en todo $\\mathbb{R}$?",
        "respuestas": {"A": "$\\frac{1}{x}$", "B": "$\\sqrt{x}$", "C": "$x^2-3x+1$", "D": "$\\tan x$"}
    },
    "MOCK-0076": {
        "pregunta": "Si $f(x) = x+1$ y $g(x) = 2x$, entonces $(f+g)(x) =$",
        "respuestas": {"A": "$3x+1$", "B": "$2x^2+2x$", "C": "$x+3$", "D": "$3x$"}
    },
    "MOCK-0077": {
        "pregunta": "Si $f(x) = x^2$ y $g(x) = x-1$, entonces $(f \\circ g)(x) =$",
        "respuestas": {"A": "$x^2-1$", "B": "$(x-1)^2$", "C": "$x^3-x^2$", "D": "$x^2+x-1$"}
    },
    "MOCK-0078": {
        "pregunta": "Si $f(x) = 3x$ y $g(x) = x+2$, entonces $(f/g)(x) =$",
        "respuestas": {"A": "$\\frac{3x}{x+2}$", "B": "$3x^2+6x$", "C": "$4x+2$", "D": "$\\frac{x+2}{3x}$"}
    },

    # =========================================================================
    # TEMA 7: Trigonometría
    # =========================================================================
    "MOCK-0079": {
        "pregunta": "Convierte $150^\\circ$ a radianes.",
        "respuestas": {"A": "$\\frac{5\\pi}{6}$", "B": "$\\frac{3\\pi}{4}$", "C": "$\\frac{2\\pi}{3}$", "D": "$\\frac{7\\pi}{6}$"}
    },
    "MOCK-0080": {
        "pregunta": "Convierte $\\frac{7\\pi}{4}$ radianes a grados.",
        "respuestas": {"A": "$225^\\circ$", "B": "$270^\\circ$", "C": "$315^\\circ$", "D": "$350^\\circ$"}
    },
    "MOCK-0081": {
        "pregunta": "Un ángulo de $\\frac{\\pi}{3}$ radianes equivale a:",
        "respuestas": {"A": "$30^\\circ$", "B": "$45^\\circ$", "C": "$60^\\circ$", "D": "$90^\\circ$"}
    },
    "MOCK-0082": {
        "pregunta": "En un triángulo rectángulo, respecto a $\\theta$, $\\operatorname{sen} \\theta$ es:",
        "respuestas": {
            "A": "$\\text{adyacente}/\\text{hipotenusa}$",
            "B": "$\\text{opuesto}/\\text{hipotenusa}$",
            "C": "$\\text{opuesto}/\\text{adyacente}$",
            "D": "$\\text{hipotenusa}/\\text{opuesto}$"
        }
    },
    "MOCK-0083": {
        "pregunta": "Si los catetos miden $5$ y $12$, la hipotenusa es:",
        "respuestas": {"A": "$13$", "B": "$15$", "C": "$17$", "D": "$7$"}
    },
    "MOCK-0084": {
        "pregunta": "Si $\\tan \\theta = \\frac{3}{4}$ y $\\theta$ es agudo, $\\cos \\theta$ es:",
        "respuestas": {"A": "$\\frac{3}{5}$", "B": "$\\frac{4}{5}$", "C": "$\\frac{5}{4}$", "D": "$\\frac{4}{3}$"}
    },
    "MOCK-0085": {
        "pregunta": "Una escalera de $10\\text{ m}$ forma $30^\\circ$ con el piso. ¿Qué altura alcanza?",
        "respuestas": {"A": "$5\\text{ m}$", "B": "$5\\sqrt{3}\\text{ m}$", "C": "$10\\sqrt{3}\\text{ m}$", "D": "$20\\text{ m}$"}
    },
    "MOCK-0086": {
        "pregunta": "Una sombra mide $6\\text{ m}$ y el ángulo de elevación es $45^\\circ$. ¿Altura del objeto?",
        "respuestas": {"A": "$3\\text{ m}$", "B": "$6\\text{ m}$", "C": "$6\\sqrt{2}\\text{ m}$", "D": "$12\\text{ m}$"}
    },
    "MOCK-0087": {
        "pregunta": "En un triángulo rectángulo, hipotenusa $8$ y ángulo $60^\\circ$. El cateto adyacente mide:",
        "respuestas": {"A": "$4$", "B": "$4\\sqrt{3}$", "C": "$8\\sqrt{3}$", "D": "$2$"}
    },
    "MOCK-0088": {
        "pregunta": "En un triángulo, $a=7$, $b=9$ y $C=60^\\circ$. Por ley de cosenos, $c^2$ es:",
        "respuestas": {"A": "$67$", "B": "$81$", "C": "$109$", "D": "$130$"}
    },
    "MOCK-0089": {
        "pregunta": "La ley de senos establece:",
        "respuestas": {
            "A": "$\\frac{a}{\\operatorname{sen} A} = \\frac{b}{\\operatorname{sen} B}$",
            "B": "$a \\cos A = b \\cos B$",
            "C": "$a^2+b^2=c^2$",
            "D": "$a+b=c$"
        }
    },
    "MOCK-0090": {
        "pregunta": "Si $A=30^\\circ$, $a=5$ y $B=90^\\circ$, entonces $b$ es:",
        "respuestas": {"A": "$5$", "B": "$5\\sqrt{2}$", "C": "$10$", "D": "$10\\sqrt{3}$"}
    },
    "MOCK-0091": {
        "pregunta": "En un triángulo, $A=40^\\circ$, $B=65^\\circ$. El ángulo $C$ es:",
        "respuestas": {"A": "$65^\\circ$", "B": "$75^\\circ$", "C": "$85^\\circ$", "D": "$105^\\circ$"}
    },
    "MOCK-0092": {
        "pregunta": "Si $a=8$, $b=10$ y $C=60^\\circ$, entonces $c$ es:",
        "respuestas": {"A": "$\\sqrt{84}$", "B": "$\\sqrt{164}$", "C": "$18$", "D": "$2$"}
    },
    "MOCK-0093": {
        "pregunta": "En un triángulo oblicuángulo, $A=30^\\circ$, $a=6$ y $B=45^\\circ$. El lado $b$ es:",
        "respuestas": {"A": "$3\\sqrt{2}$", "B": "$6\\sqrt{2}$", "C": "$12$", "D": "$6$"}
    },
    "MOCK-0094": {
        "pregunta": "El valor de $\\operatorname{sen} 150^\\circ$ es:",
        "respuestas": {"A": "$-\\frac{1}{2}$", "B": "$\\frac{1}{2}$", "C": "$-\\frac{\\sqrt{3}}{2}$", "D": "$\\frac{\\sqrt{3}}{2}$"}
    },
    "MOCK-0095": {
        "pregunta": "El valor de $\\cos 210^\\circ$ es:",
        "respuestas": {"A": "$\\frac{\\sqrt{3}}{2}$", "B": "$-\\frac{\\sqrt{3}}{2}$", "C": "$\\frac{1}{2}$", "D": "$-\\frac{1}{2}$"}
    },
    "MOCK-0096": {
        "pregunta": "La expresión $\\tan(\\pi+\\theta)$ es igual a:",
        "respuestas": {"A": "$-\\tan \\theta$", "B": "$\\tan \\theta$", "C": "$\\cot \\theta$", "D": "$-\\cot \\theta$"}
    },
    "MOCK-0097": {
        "pregunta": "En el círculo unitario, el punto para $\\theta = \\frac{\\pi}{2}$ es:",
        "respuestas": {"A": "$(1, 0)$", "B": "$(0, 1)$", "C": "$(-1, 0)$", "D": "$(0, -1)$"}
    },
    "MOCK-0098": {
        "pregunta": "La coordenada $x$ del punto del círculo unitario es:",
        "respuestas": {"A": "$\\operatorname{sen} \\theta$", "B": "$\\cos \\theta$", "C": "$\\tan \\theta$", "D": "$\\sec \\theta$"}
    },
    "MOCK-0099": {
        "pregunta": "El punto $(-1, 0)$ corresponde al ángulo:",
        "respuestas": {"A": "$0$", "B": "$\\frac{\\pi}{2}$", "C": "$\\pi$", "D": "$\\frac{3\\pi}{2}$"}
    },
    "MOCK-0100": {
        "pregunta": "El dominio de $f(x) = \\operatorname{sen} x$ es:",
        "respuestas": {"A": "$[-1, 1]$", "B": "$\\mathbb{R}$", "C": "$\\mathbb{R} \\setminus \\{0\\}$", "D": "$[0, \\infty)$"}
    },
    "MOCK-0101": {
        "pregunta": "El rango de $f(x) = \\cos x$ es:",
        "respuestas": {"A": "$\\mathbb{R}$", "B": "$[0, 1]$", "C": "$[-1, 1]$", "D": "$(-1, 1)$"}
    },
    "MOCK-0102": {
        "pregunta": "El dominio de $f(x) = \\tan x$ excluye los valores:",
        "respuestas": {"A": "$x = k\\pi$", "B": "$x = \\frac{\\pi}{2} + k\\pi$", "C": "$x = 2k\\pi$", "D": "$x = \\frac{\\pi}{4} + k\\pi$"}
    },
    "MOCK-0103": {
        "pregunta": "La amplitud de $y = 4\\operatorname{sen} x$ es:",
        "respuestas": {"A": "$1$", "B": "$2$", "C": "$4$", "D": "$2\\pi$"}
    },
    "MOCK-0104": {
        "pregunta": "El periodo de $y = \\cos(3x)$ es:",
        "respuestas": {"A": "$2\\pi$", "B": "$3\\pi$", "C": "$\\frac{2\\pi}{3}$", "D": "$\\frac{\\pi}{3}$"}
    },
    "MOCK-0105": {
        "pregunta": "La amplitud y periodo de $y = -2\\operatorname{sen}(x/2)$ son:",
        "respuestas": {"A": "$2$ y $4\\pi$", "B": "$-2$ y $4\\pi$", "C": "$2$ y $\\pi$", "D": "$1/2$ y $2\\pi$"}
    },
    "MOCK-0106": {
        "pregunta": "$y = \\operatorname{sen}\\left(x - \\frac{\\pi}{3}\\right)$ se desplaza:",
        "respuestas": {"A": "$\\pi/3$ a la derecha", "B": "$\\pi/3$ a la izquierda", "C": "$3\\pi$ a la derecha", "D": "$\\pi$ a la izquierda"}
    },
    "MOCK-0107": {
        "pregunta": "$y = \\cos\\left(x + \\frac{\\pi}{4}\\right)$ se desplaza:",
        "respuestas": {"A": "$\\pi/4$ a la derecha", "B": "$\\pi/4$ a la izquierda", "C": "$4\\pi$ a la izquierda", "D": "No se desplaza"}
    },
    "MOCK-0108": {
        "pregunta": "¿Cuál función tiene desplazamiento de $\\frac{\\pi}{2}$ a la derecha?",
        "respuestas": {"A": "$\\operatorname{sen}\\left(x+\\frac{\\pi}{2}\\right)$", "B": "$\\operatorname{sen}\\left(x-\\frac{\\pi}{2}\\right)$", "C": "$\\operatorname{sen}(2x)$", "D": "$\\operatorname{sen} x + \\frac{\\pi}{2}$"}
    },
    "MOCK-0109": {
        "pregunta": "Las asíntotas verticales de $\\tan x$ son:",
        "respuestas": {"A": "$x = k\\pi$", "B": "$x = \\frac{\\pi}{2} + k\\pi$", "C": "$y = \\frac{\\pi}{2} + k\\pi$", "D": "$x = 2k\\pi$"}
    },
    "MOCK-0110": {
        "pregunta": "Las asíntotas verticales de $\\sec x$ ocurren cuando:",
        "respuestas": {"A": "$\\operatorname{sen} x = 0$", "B": "$\\cos x = 0$", "C": "$\\tan x = 0$", "D": "$x = 0$ solamente"}
    },
    "MOCK-0111": {
        "pregunta": "Una asíntota vertical de $\\csc x$ es:",
        "respuestas": {"A": "$x = \\frac{\\pi}{2}$", "B": "$x = \\pi$", "C": "$x = \\frac{\\pi}{4}$", "D": "$x = \\frac{3\\pi}{2}$"}
    },

    # =========================================================================
    # TEMA 8: Funciones exponenciales y logarítmicas
    # =========================================================================
    "MOCK-0112": {
        "pregunta": "El dominio de $\\log(x+4)$ es:",
        "respuestas": {"A": "$x > -4$", "B": "$x \\ge -4$", "C": "$x < 4$", "D": "$\\mathbb{R}$"}
    },
    "MOCK-0113": {
        "pregunta": "El rango de $e^x - 3$ es:",
        "respuestas": {"A": "$(-3, \\infty)$", "B": "$[-3, \\infty)$", "C": "$(0, \\infty)$", "D": "$\\mathbb{R}$"}
    },
    "MOCK-0114": {
        "pregunta": "El dominio de $2^x$ es:",
        "respuestas": {"A": "$(0, \\infty)$", "B": "$[0, \\infty)$", "C": "$\\mathbb{R}$", "D": "$\\mathbb{R} \\setminus \\{0\\}$"}
    },
    "MOCK-0115": {
        "pregunta": "La asíntota vertical de $\\log_2(x-5)$ es:",
        "respuestas": {"A": "$x = 0$", "B": "$x = 5$", "C": "$y = 5$", "D": "$y = 0$"}
    },
    "MOCK-0116": {
        "pregunta": "La asíntota horizontal de $3^x+2$ es:",
        "respuestas": {"A": "$x = 2$", "B": "$y = 0$", "C": "$y = 2$", "D": "$x = 0$"}
    },
    "MOCK-0117": {
        "pregunta": "La gráfica de $y = (1/2)^x$ es:",
        "respuestas": {"A": "Exponencial creciente", "B": "Exponencial decreciente", "C": "Logarítmica creciente", "D": "Recta"}
    },

    # =========================================================================
    # TEMA 9: Recta
    # =========================================================================
    "MOCK-0118": {
        "pregunta": "Distancia entre $(1,2)$ y $(4,6)$:",
        "respuestas": {"A": "$3$", "B": "$4$", "C": "$5$", "D": "$7$"}
    },
    "MOCK-0119": {
        "pregunta": "Distancia entre $(-2,3)$ y $(-2,-5)$:",
        "respuestas": {"A": "$2$", "B": "$5$", "C": "$8$", "D": "$10$"}
    },
    "MOCK-0120": {
        "pregunta": "Distancia entre $(0,0)$ y $(6,8)$:",
        "respuestas": {"A": "$7$", "B": "$10$", "C": "$12$", "D": "$14$"}
    },
    "MOCK-0121": {
        "pregunta": "Punto medio entre $(2,-1)$ y $(8,5)$:",
        "respuestas": {"A": "$(5, 2)$", "B": "$(3, 4)$", "C": "$(10, 4)$", "D": "$(5, 3)$"}
    },
    "MOCK-0122": {
        "pregunta": "El punto que divide al segmento $A(0,0)$, $B(9,6)$ en razón $AP:PB = 1:2$ es:",
        "respuestas": {"A": "$(3, 2)$", "B": "$(6, 4)$", "C": "$(4.5, 3)$", "D": "$(1, 2)$"}
    },
    "MOCK-0123": {
        "pregunta": "Punto medio de $A(2m, m+2)$ y $B(4m, m-2)$:",
        "respuestas": {"A": "$(3m, m)$", "B": "$(6m, 2m)$", "C": "$(m, 3m)$", "D": "$(2m, m)$"}
    },
    "MOCK-0124": {
        "pregunta": "Pendiente de la recta que pasa por $(1,4)$ y $(5,12)$:",
        "respuestas": {"A": "$1/2$", "B": "$2$", "C": "$4$", "D": "$-2$"}
    },
    "MOCK-0125": {
        "pregunta": "Pendiente de $2x+4y-7=0$:",
        "respuestas": {"A": "$2$", "B": "$-2$", "C": "$1/2$", "D": "$-1/2$"}
    },
    "MOCK-0126": {
        "pregunta": "Una recta horizontal tiene pendiente:",
        "respuestas": {"A": "$0$", "B": "$1$", "C": "$-1$", "D": "Indefinida"}
    },
    "MOCK-0127": {
        "pregunta": "Recta con pendiente $3$ y ordenada al origen $-2$:",
        "respuestas": {"A": "$y = 3x-2$", "B": "$y = -2x+3$", "C": "$3y = x-2$", "D": "$y = 3x+2$"}
    },
    "MOCK-0128": {
        "pregunta": "Recta que pasa por $(2,5)$ con pendiente $-1$:",
        "respuestas": {"A": "$y = -x+7$", "B": "$y = x+3$", "C": "$y = -x+3$", "D": "$y = 2x+1$"}
    },
    "MOCK-0129": {
        "pregunta": "La forma general de $y = 2x+4$ es:",
        "respuestas": {"A": "$2x-y+4=0$", "B": "$2x-y-4=0$", "C": "$x-2y+4=0$", "D": "$2x+y+4=0$"}
    },
    "MOCK-0130": {
        "pregunta": "Una recta paralela a $y = 4x-1$ tiene pendiente:",
        "respuestas": {"A": "$-4$", "B": "$1/4$", "C": "$4$", "D": "$-1/4$"}
    },
    "MOCK-0131": {
        "pregunta": "Una recta perpendicular a $y = -2x+3$ tiene pendiente:",
        "respuestas": {"A": "$-2$", "B": "$2$", "C": "$1/2$", "D": "$-1/2$"}
    },
    "MOCK-0132": {
        "pregunta": "Las rectas $3x-y=2$ y $6x-2y=5$ son:",
        "respuestas": {"A": "Paralelas", "B": "Perpendiculares", "C": "Coincidentes", "D": "Verticales"}
    },
    "MOCK-0133": {
        "pregunta": "Distancia del punto $(0,0)$ a la recta $3x+4y-10=0$:",
        "respuestas": {"A": "$1$", "B": "$2$", "C": "$5$", "D": "$10$"}
    },
    "MOCK-0134": {
        "pregunta": "Distancia del punto $(2,1)$ a la recta $x-y+3=0$:",
        "respuestas": {"A": "$2\\sqrt{2}$", "B": "$\\sqrt{2}$", "C": "$4$", "D": "$1$"}
    },
    "MOCK-0135": {
        "pregunta": "Distancia del punto $(-1,2)$ a la recta $y = 5$:",
        "respuestas": {"A": "$2$", "B": "$3$", "C": "$4$", "D": "$5$"}
    },
    "MOCK-0136": {
        "pregunta": "La mediana de un triángulo une un vértice con:",
        "respuestas": {
            "A": "El punto medio del lado opuesto",
            "B": "El ortocentro",
            "C": "Un ángulo recto",
            "D": "El centro de una circunferencia"
        }
    },
    "MOCK-0137": {
        "pregunta": "El punto de intersección de las alturas de un triángulo es:",
        "respuestas": {"A": "Baricentro", "B": "Circuncentro", "C": "Ortocentro", "D": "Incentro"}
    },
    "MOCK-0138": {
        "pregunta": "La mediatriz del segmento entre $(0,0)$ y $(4,0)$ es la recta:",
        "respuestas": {"A": "$x = 0$", "B": "$x = 2$", "C": "$y = 2$", "D": "$y = 0$"}
    },

    # =========================================================================
    # TEMA 10: Circunferencia
    # =========================================================================
    "MOCK-0139": {
        "pregunta": "Una circunferencia es el lugar geométrico cuya distancia a un punto fijo es:",
        "respuestas": {"A": "Variable", "B": "Constante", "C": "Cero", "D": "Infinita"}
    },
    "MOCK-0140": {
        "pregunta": "Si el centro es $C$ y el radio $r$, un punto $P$ pertenece a la circunferencia cuando:",
        "respuestas": {"A": "$d(P,C) < r$", "B": "$d(P,C) = r$", "C": "$d(P,C) > r$", "D": "$d(P,C) = 2r$"}
    },
    "MOCK-0141": {
        "pregunta": "El lugar geométrico de puntos a $6$ unidades de $(2,-1)$ es:",
        "respuestas": {"A": "Una recta", "B": "Una parábola", "C": "Una circunferencia", "D": "Una elipse"}
    },
    "MOCK-0142": {
        "pregunta": "Circunferencia con centro en $(0,0)$ y radio $5$:",
        "respuestas": {"A": "$x^2+y^2=5$", "B": "$x^2+y^2=25$", "C": "$(x-5)^2+y^2=25$", "D": "$x^2-y^2=25$"}
    },
    "MOCK-0143": {
        "pregunta": "El radio de $x^2+y^2-49=0$ es:",
        "respuestas": {"A": "$7$", "B": "$49$", "C": "$\\sqrt{7}$", "D": "$14$"}
    },
    "MOCK-0144": {
        "pregunta": "¿Cuál circunferencia tiene centro en el origen?",
        "respuestas": {"A": "$(x-1)^2+y^2=9$", "B": "$x^2+y^2=16$", "C": "$x^2+(y+2)^2=4$", "D": "$x^2-y^2=1$"}
    },
    "MOCK-0145": {
        "pregunta": "Circunferencia con centro $(3,-2)$ y radio $4$:",
        "respuestas": {"A": "$(x-3)^2+(y+2)^2=16$", "B": "$(x+3)^2+(y-2)^2=16$", "C": "$(x-3)^2+(y-2)^2=4$", "D": "$x^2+y^2=16$"}
    },
    "MOCK-0146": {
        "pregunta": "El centro de $(x+5)^2+(y-1)^2=9$ es:",
        "respuestas": {"A": "$(5, -1)$", "B": "$(-5, 1)$", "C": "$(-5, -1)$", "D": "$(5, 1)$"}
    },
    "MOCK-0147": {
        "pregunta": "La forma general de $(x-1)^2+(y+2)^2=4$ es:",
        "respuestas": {"A": "$x^2+y^2-2x+4y+1=0$", "B": "$x^2+y^2+2x-4y+1=0$", "C": "$x^2+y^2-2x+4y-4=0$", "D": "$x^2+y^2=4$"}
    },
    "MOCK-0148": {
        "pregunta": "Centro y radio de $x^2+y^2-6x+4y-12=0$:",
        "respuestas": {"A": "$C(3, -2),\\, r=5$", "B": "$C(-3, 2),\\, r=5$", "C": "$C(3, 2),\\, r=1$", "D": "$C(-3, -2),\\, r=5$"}
    },
    "MOCK-0149": {
        "pregunta": "El diámetro de una circunferencia de radio $7$ es:",
        "respuestas": {"A": "$3.5$", "B": "$7$", "C": "$14$", "D": "$49$"}
    },
    "MOCK-0150": {
        "pregunta": "Los extremos de un diámetro son $(-2,0)$ y $(6,0)$. El centro es:",
        "respuestas": {"A": "$(2, 0)$", "B": "$(4, 0)$", "C": "$(2, 3)$", "D": "$(-4, 0)$"}
    },

    # =========================================================================
    # TEMA 11: Parábola
    # =========================================================================
    "MOCK-0151": {
        "pregunta": "Una parábola es el lugar geométrico de puntos equidistantes de:",
        "respuestas": {"A": "Dos focos", "B": "Un foco y una directriz", "C": "Un centro y una recta", "D": "Dos rectas"}
    },
    "MOCK-0152": {
        "pregunta": "En una parábola, el punto fijo de referencia se llama:",
        "respuestas": {"A": "Centro", "B": "Vértice", "C": "Foco", "D": "Radio"}
    },
    "MOCK-0153": {
        "pregunta": "La recta fija usada en la definición de parábola se llama:",
        "respuestas": {"A": "Asíntota", "B": "Directriz", "C": "Tangente", "D": "Eje mayor"}
    },
    "MOCK-0154": {
        "pregunta": "Parábola con vértice en el origen y foco $(3,0)$:",
        "respuestas": {"A": "$y^2 = 12x$", "B": "$x^2 = 12y$", "C": "$y^2 = -12x$", "D": "$x^2 = -12y$"}
    },
    "MOCK-0155": {
        "pregunta": "El foco de $x^2 = 8y$ es:",
        "respuestas": {"A": "$(2, 0)$", "B": "$(0, 2)$", "C": "$(0, 8)$", "D": "$(-2, 0)$"}
    },
    "MOCK-0156": {
        "pregunta": "La directriz de $y^2 = -4x$ es:",
        "respuestas": {"A": "$x = -1$", "B": "$x = 1$", "C": "$y = 1$", "D": "$y = -1$"}
    },
    "MOCK-0157": {
        "pregunta": "Parábola con vértice $(2,-1)$ y parámetro $p=3$, eje vertical:",
        "respuestas": {"A": "$(x-2)^2 = 12(y+1)$", "B": "$(y+1)^2 = 12(x-2)$", "C": "$(x+2)^2 = 3(y-1)$", "D": "$(x-2)^2 = -12(y+1)$"}
    },
    "MOCK-0158": {
        "pregunta": "El vértice de $(y-4)^2 = 8(x+1)$ es:",
        "respuestas": {"A": "$(4, -1)$", "B": "$(-1, 4)$", "C": "$(1, -4)$", "D": "$(-4, 1)$"}
    },
    "MOCK-0159": {
        "pregunta": "Parábola con vértice $(-2,3)$ y foco $(-2,1)$:",
        "respuestas": {"A": "$(x+2)^2 = -8(y-3)$", "B": "$(y-3)^2 = -8(x+2)$", "C": "$(x-2)^2 = 8(y+3)$", "D": "$(x+2)^2 = 8(y-3)$"}
    },
    "MOCK-0160": {
        "pregunta": "En la parábola $y^2 = 16x$, el lado recto mide:",
        "respuestas": {"A": "$4$", "B": "$8$", "C": "$16$", "D": "$32$"}
    },
    "MOCK-0161": {
        "pregunta": "Vértice y foco de $(x-1)^2 = 12(y+2)$:",
        "respuestas": {"A": "$V(1, -2),\\, F(1, 1)$", "B": "$V(-1, 2),\\, F(-1, 5)$", "C": "$V(1, 2),\\, F(4, 2)$", "D": "$V(1, -2),\\, F(4, -2)$"}
    },
    "MOCK-0162": {
        "pregunta": "El eje de simetría de $y^2-6y-8x+9=0$ es:",
        "respuestas": {"A": "$x = 3$", "B": "$y = 3$", "C": "$x = -3$", "D": "$y = -3$"}
    },

    # =========================================================================
    # TEMA 12: Elipse
    # =========================================================================
    "MOCK-0163": {
        "pregunta": "Una elipse es el lugar geométrico cuya suma de distancias a dos focos es:",
        "respuestas": {"A": "Constante", "B": "Cero", "C": "Variable", "D": "Infinita"}
    },
    "MOCK-0164": {
        "pregunta": "Si los focos de una elipse coinciden, se obtiene:",
        "respuestas": {"A": "Una parábola", "B": "Una circunferencia", "C": "Una hipérbola", "D": "Una recta"}
    },
    "MOCK-0165": {
        "pregunta": "En una elipse no circular, la excentricidad cumple:",
        "respuestas": {"A": "$e = 0$", "B": "$0 < e < 1$", "C": "$e = 1$", "D": "$e > 1$"}
    },
    "MOCK-0166": {
        "pregunta": "En una elipse con semiejes $a=5$ y $b=3$, la distancia focal $c$ es:",
        "respuestas": {"A": "$2$", "B": "$4$", "C": "$\\sqrt{34}$", "D": "$8$"}
    },
    "MOCK-0167": {
        "pregunta": "En una elipse, la relación pitagórica correcta entre parámetros es:",
        "respuestas": {"A": "$c^2 = a^2+b^2$", "B": "$a^2 = b^2+c^2$", "C": "$b^2 = a^2+c^2$", "D": "$a = b+c$"}
    },
    "MOCK-0168": {
        "pregunta": "Si $a=13$ y $c=5$ en una elipse, el semieje menor $b$ es:",
        "respuestas": {"A": "$8$", "B": "$10$", "C": "$12$", "D": "$18$"}
    },
    "MOCK-0169": {
        "pregunta": "Elipse horizontal con centro en el origen, $a=5$, $b=3$:",
        "respuestas": {"A": "$\\frac{x^2}{25}+\\frac{y^2}{9}=1$", "B": "$\\frac{x^2}{9}+\\frac{y^2}{25}=1$", "C": "$\\frac{x^2}{5}+\\frac{y^2}{3}=1$", "D": "$\\frac{x^2}{25}-\\frac{y^2}{9}=1$"}
    },
    "MOCK-0170": {
        "pregunta": "Los vértices de $\\frac{x^2}{16}+\\frac{y^2}{4}=1$ son:",
        "respuestas": {"A": "$(0, \\pm 4)$", "B": "$(\\pm 4, 0)$", "C": "$(\\pm 2, 0)$", "D": "$(0, \\pm 2)$"}
    },
    "MOCK-0171": {
        "pregunta": "El eje mayor de $\\frac{x^2}{9}+\\frac{y^2}{36}=1$ es:",
        "respuestas": {"A": "Horizontal", "B": "Vertical", "C": "Inclinado", "D": "No existe"}
    },
    "MOCK-0172": {
        "pregunta": "Elipse con centro $(2,-1)$, eje mayor horizontal, $a=4$, $b=2$:",
        "respuestas": {"A": "$\\frac{(x-2)^2}{16}+\\frac{(y+1)^2}{4}=1$", "B": "$\\frac{(x+2)^2}{16}+\\frac{(y-1)^2}{4}=1$", "C": "$\\frac{(x-2)^2}{4}+\\frac{(y+1)^2}{16}=1$", "D": "$\\frac{x^2}{16}+\\frac{y^2}{4}=1$"}
    },
    "MOCK-0173": {
        "pregunta": "Centro de la elipse $\\frac{(x+3)^2}{25}+\\frac{(y-4)^2}{9}=1$:",
        "respuestas": {"A": "$(3, -4)$", "B": "$(-3, 4)$", "C": "$(-3, -4)$", "D": "$(3, 4)$"}
    },
    "MOCK-0174": {
        "pregunta": "La elipse $\\frac{(x-1)^2}{9}+\\frac{(y+2)^2}{16}=1$ tiene eje mayor:",
        "respuestas": {"A": "Horizontal", "B": "Vertical", "C": "Inclinado", "D": "Nulo"}
    },
    "MOCK-0175": {
        "pregunta": "Focos de $\\frac{x^2}{25}+\\frac{y^2}{9}=1$:",
        "respuestas": {"A": "$(\\pm 4, 0)$", "B": "$(0, \\pm 4)$", "C": "$(\\pm 5, 0)$", "D": "$(0, \\pm 3)$"}
    },
    "MOCK-0176": {
        "pregunta": "La longitud del eje mayor de $\\frac{x^2}{36}+\\frac{y^2}{16}=1$ es:",
        "respuestas": {"A": "$6$", "B": "$8$", "C": "$12$", "D": "$16$"}
    },
    "MOCK-0177": {
        "pregunta": "La excentricidad de $\\frac{x^2}{25}+\\frac{y^2}{16}=1$ es:",
        "respuestas": {"A": "$\\frac{3}{5}$", "B": "$\\frac{4}{5}$", "C": "$\\frac{1}{5}$", "D": "$\\frac{5}{3}$"}
    },

    # =========================================================================
    # TEMA 13: Hipérbola
    # =========================================================================
    "MOCK-0178": {
        "pregunta": "Una hipérbola es el lugar geométrico cuya diferencia absoluta de distancias a dos focos es:",
        "respuestas": {"A": "Constante", "B": "Cero", "C": "Variable", "D": "Igual a la suma"}
    },
    "MOCK-0179": {
        "pregunta": "La excentricidad de una hipérbola cumple:",
        "respuestas": {"A": "$e = 0$", "B": "$0 < e < 1$", "C": "$e = 1$", "D": "$e > 1$"}
    },
    "MOCK-0180": {
        "pregunta": "Una hipérbola consta de:",
        "respuestas": {"A": "Una rama", "B": "Dos ramas", "C": "Ningún foco", "D": "Un solo vértice"}
    },
    "MOCK-0181": {
        "pregunta": "En una hipérbola con $a=3$ y $b=4$, la distancia focal $c$ es:",
        "respuestas": {"A": "$1$", "B": "$5$", "C": "$7$", "D": "$\\sqrt{7}$"}
    },
    "MOCK-0182": {
        "pregunta": "En una hipérbola, la relación pitagórica correcta entre parámetros es:",
        "respuestas": {"A": "$c^2 = a^2+b^2$", "B": "$a^2 = b^2+c^2$", "C": "$b^2 = a^2+c^2$", "D": "$c = a-b$"}
    },
    "MOCK-0183": {
        "pregunta": "Si $c=13$ y $a=5$ en una hipérbola, el semieje conjugado $b$ es:",
        "respuestas": {"A": "$8$", "B": "$10$", "C": "$12$", "D": "$18$"}
    },
    "MOCK-0184": {
        "pregunta": "Hipérbola horizontal con centro en el origen, $a=4$, $b=3$:",
        "respuestas": {"A": "$\\frac{x^2}{16}-\\frac{y^2}{9}=1$", "B": "$\\frac{y^2}{16}-\\frac{x^2}{9}=1$", "C": "$\\frac{x^2}{4}-\\frac{y^2}{3}=1$", "D": "$\\frac{x^2}{16}+\\frac{y^2}{9}=1$"}
    },
    "MOCK-0185": {
        "pregunta": "Los vértices de $\\frac{y^2}{25}-\\frac{x^2}{9}=1$ son:",
        "respuestas": {"A": "$(\\pm 5, 0)$", "B": "$(0, \\pm 5)$", "C": "$(\\pm 3, 0)$", "D": "$(0, \\pm 3)$"}
    },
    "MOCK-0186": {
        "pregunta": "Las asíntotas de $\\frac{x^2}{4}-\\frac{y^2}{9}=1$ son:",
        "respuestas": {"A": "$y = \\pm \\frac{3}{2}x$", "B": "$y = \\pm \\frac{2}{3}x$", "C": "$y = \\pm 6x$", "D": "$x = \\pm 2$"}
    },
    "MOCK-0187": {
        "pregunta": "Hipérbola con centro $(1,-2)$, eje horizontal, $a=3$, $b=2$:",
        "respuestas": {"A": "$\\frac{(x-1)^2}{9}-\\frac{(y+2)^2}{4}=1$", "B": "$\\frac{(y+2)^2}{9}-\\frac{(x-1)^2}{4}=1$", "C": "$\\frac{(x+1)^2}{9}-\\frac{(y-2)^2}{4}=1$", "D": "$\\frac{x^2}{9}-\\frac{y^2}{4}=1$"}
    },
    "MOCK-0188": {
        "pregunta": "Centro de $\\frac{(x+4)^2}{16}-\\frac{(y-3)^2}{25}=1$:",
        "respuestas": {"A": "$(4, -3)$", "B": "$(-4, 3)$", "C": "$(-4, -3)$", "D": "$(4, 3)$"}
    },
    "MOCK-0189": {
        "pregunta": "La hipérbola $\\frac{(y-1)^2}{4}-\\frac{(x+2)^2}{9}=1$ abre hacia:",
        "respuestas": {"A": "Izquierda y derecha", "B": "Arriba y abajo", "C": "En cuatro direcciones", "D": "No abre"}
    },
    "MOCK-0190": {
        "pregunta": "Focos de $\\frac{x^2}{9}-\\frac{y^2}{16}=1$:",
        "respuestas": {"A": "$(\\pm 5, 0)$", "B": "$(0, \\pm 5)$", "C": "$(\\pm 3, 0)$", "D": "$(0, \\pm 4)$"}
    },
    "MOCK-0191": {
        "pregunta": "La longitud del eje transverso de $\\frac{x^2}{25}-\\frac{y^2}{9}=1$ es:",
        "respuestas": {"A": "$5$", "B": "$6$", "C": "$10$", "D": "$18$"}
    },
    "MOCK-0192": {
        "pregunta": "La excentricidad de $\\frac{x^2}{9}-\\frac{y^2}{16}=1$ es:",
        "respuestas": {"A": "$\\frac{3}{5}$", "B": "$\\frac{4}{3}$", "C": "$\\frac{5}{3}$", "D": "$\\frac{5}{4}$"}
    },

    # =========================================================================
    # TEMA 14: Ecuación general de segundo grado
    # =========================================================================
    "MOCK-0193": {
        "pregunta": "¿Cuál no es una cónica no degenerada?",
        "respuestas": {"A": "Circunferencia", "B": "Elipse", "C": "Triángulo", "D": "Hipérbola"}
    },
    "MOCK-0194": {
        "pregunta": "La intersección de un plano paralelo a una generatriz de un cono produce una:",
        "respuestas": {"A": "Circunferencia", "B": "Parábola", "C": "Elipse", "D": "Recta"}
    },
    "MOCK-0195": {
        "pregunta": "La circunferencia es un caso particular de:",
        "respuestas": {"A": "Parábola", "B": "Hipérbola", "C": "Elipse", "D": "Recta"}
    },
    "MOCK-0196": {
        "pregunta": "La ecuación general de segundo grado en $x, y$ es:",
        "respuestas": {"A": "$Ax^2+Bxy+Cy^2+Dx+Ey+F=0$", "B": "$Ax+B=0$", "C": "$Ax^3+By^3=0$", "D": "$Ax^2+Bx+C=0$"}
    },
    "MOCK-0197": {
        "pregunta": "En $Ax^2+Bxy+Cy^2+Dx+Ey+F=0$, el término que indica posible rotación es:",
        "respuestas": {"A": "$Dx$", "B": "$Ey$", "C": "$Bxy$", "D": "$F$"}
    },
    "MOCK-0198": {
        "pregunta": "Si $B=0$, los ejes de la cónica son, en general:",
        "respuestas": {"A": "Paralelos a los ejes coordenados", "B": "Siempre oblicuos", "C": "Siempre verticales", "D": "Inexistentes"}
    },
    "MOCK-0199": {
        "pregunta": "Si $B^2-4AC < 0$, la cónica puede ser una:",
        "respuestas": {"A": "Hipérbola", "B": "Parábola", "C": "Elipse", "D": "Recta"}
    },
    "MOCK-0200": {
        "pregunta": "Si $B^2-4AC = 0$, la cónica no degenerada es una:",
        "respuestas": {"A": "Circunferencia", "B": "Parábola", "C": "Elipse", "D": "Hipérbola"}
    },
    "MOCK-0201": {
        "pregunta": "Si $B^2-4AC > 0$, la cónica es una:",
        "respuestas": {"A": "Elipse", "B": "Circunferencia", "C": "Parábola", "D": "Hipérbola"}
    },
    "MOCK-0202": {
        "pregunta": "Trasladar el origen a $(h,k)$ equivale a usar la transformación:",
        "respuestas": {"A": "$x=X+h,\\, y=Y+k$", "B": "$x=X-h,\\, y=Y-k$", "C": "$x=hX,\\, y=kY$", "D": "$x=X+k,\\, y=Y+h$"}
    },
    "MOCK-0203": {
        "pregunta": "La circunferencia $x^2+y^2=9$ trasladada al centro $(2,-1)$ es:",
        "respuestas": {"A": "$(x-2)^2+(y+1)^2=9$", "B": "$(x+2)^2+(y-1)^2=9$", "C": "$(x-2)^2+(y-1)^2=3$", "D": "$x^2+y^2=9$"}
    },
    "MOCK-0204": {
        "pregunta": "La traslación de ejes cambia:",
        "respuestas": {
            "A": "La forma de la cónica",
            "B": "Su tamaño siempre",
            "C": "Las coordenadas respecto del nuevo origen",
            "D": "La excentricidad"
        }
    },

    # =========================================================================
    # TEMA 15: Límites y continuidad
    # =========================================================================
    "MOCK-0205": {
        "pregunta": "Si $f(x)$ toma valores cada vez más cercanos a $5$ cuando $x$ se aproxima a $2$, entonces intuitivamente:",
        "respuestas": {"A": "$\\lim_{x \\to 2} f(x) = 5$", "B": "$f(2) = 0$", "C": "$\\lim_{x \\to 5} f(x) = 2$", "D": "No existe límite"}
    },
    "MOCK-0206": {
        "pregunta": "Para $f(x) = \\frac{x^2-4}{x-2}$, con $x \\neq 2$, cuando $x \\to 2$ los valores se aproximan a:",
        "respuestas": {"A": "$0$", "B": "$2$", "C": "$4$", "D": "No existe"}
    },
    "MOCK-0207": {
        "pregunta": "Que exista $\\lim_{x \\to a} f(x) = L$ significa que $f(x)$:",
        "respuestas": {
            "A": "Vale $L$ solo en $x=a$",
            "B": "Se aproxima a $L$ cuando $x$ se aproxima a $a$",
            "C": "Es constante",
            "D": "Nunca vale $L$"
        }
    },
    "MOCK-0208": {
        "pregunta": "La definición $\\varepsilon$-$\\delta$ de $\\lim_{x \\to a} f(x) = L$ exige que para todo $\\varepsilon > 0$ exista $\\delta > 0$ tal que:",
        "respuestas": {
            "A": "$|x-a| < \\varepsilon$",
            "B": "$0 < |x-a| < \\delta \\implies |f(x)-L| < \\varepsilon$",
            "C": "$|f(x)| < \\delta$",
            "D": "$x = a$"
        }
    },
    "MOCK-0209": {
        "pregunta": "En la definición formal de límite, $\\delta$ controla la cercanía de:",
        "respuestas": {"A": "$f(x)$ a $L$", "B": "$x$ a $a$", "C": "$L$ a cero", "D": "$\\varepsilon$ a infinito"}
    },
    "MOCK-0210": {
        "pregunta": "En la definición formal de límite, $\\varepsilon$ mide la tolerancia en:",
        "respuestas": {"A": "La variable $x$", "B": "Los valores $f(x)$ respecto de $L$", "C": "El punto $a$ respecto de cero", "D": "El dominio completo"}
    },
    "MOCK-0211": {
        "pregunta": "Si $\\lim f = 3$ y $\\lim g = 4$, entonces $\\lim(f+g) =$",
        "respuestas": {"A": "$1$", "B": "$7$", "C": "$12$", "D": "$\\frac{3}{4}$"}
    },
    "MOCK-0212": {
        "pregunta": "Si $\\lim f = -2$, entonces $\\lim[5f] =$",
        "respuestas": {"A": "$-10$", "B": "$3$", "C": "$10$", "D": "$-2$"}
    },
    "MOCK-0213": {
        "pregunta": "Si $\\lim f = 6$ y $\\lim g = 2$, entonces $\\lim(f/g) =$",
        "respuestas": {"A": "$3$", "B": "$4$", "C": "$8$", "D": "$12$"}
    },
    "MOCK-0214": {
        "pregunta": "Calcula: $\\lim_{x \\to 2} (3x+1)$.",
        "respuestas": {"A": "$5$", "B": "$6$", "C": "$7$", "D": "$8$"}
    },
    "MOCK-0215": {
        "pregunta": "Calcula: $\\lim_{x \\to 3} \\frac{x^2-9}{x-3}$.",
        "respuestas": {"A": "$0$", "B": "$3$", "C": "$6$", "D": "$9$"}
    },
    "MOCK-0216": {
        "pregunta": "Calcula: $\\lim_{x \\to 0} \\frac{\\operatorname{sen} x}{x}$.",
        "respuestas": {"A": "$0$", "B": "$1$", "C": "$-1$", "D": "No existe"}
    },
    "MOCK-0217": {
        "pregunta": "La sustitución directa en $\\lim_{x \\to 2} \\frac{x^2-4}{x-2}$ produce la forma indeterminada:",
        "respuestas": {"A": "$\\frac{0}{0}$", "B": "$\\frac{\\infty}{\\infty}$", "C": "$0 \\cdot \\infty$", "D": "$\\infty - \\infty$"}
    },
    "MOCK-0218": {
        "pregunta": "La forma indeterminada obtenida en $\\lim_{x \\to \\infty} \\frac{2x^2+1}{x^2-3}$ es:",
        "respuestas": {"A": "$\\frac{0}{0}$", "B": "$\\frac{\\infty}{\\infty}$", "C": "$1^\\infty$", "D": "$\\infty - \\infty$"}
    },
    "MOCK-0219": {
        "pregunta": "¿Cuál de las siguientes es una forma indeterminada?",
        "respuestas": {"A": "$\\frac{5}{0}$", "B": "$\\frac{0}{0}$", "C": "$\\frac{3}{2}$", "D": "$\\infty + \\infty$"}
    },
    "MOCK-0220": {
        "pregunta": "Para que $f$ sea continua en $x=a$ debe cumplirse:",
        "respuestas": {"A": "$f(a) = 0$", "B": "$\\lim_{x \\to a} f(x) = f(a)$", "C": "$f'(a) = 0$", "D": "$a = 0$"}
    },
    "MOCK-0221": {
        "pregunta": "La función $f(x) = \\frac{1}{x+3}$ es discontinua en:",
        "respuestas": {"A": "$x = 3$", "B": "$x = -3$", "C": "$x = 0$", "D": "Todo $\\mathbb{R}$"}
    },
    "MOCK-0222": {
        "pregunta": "¿Cuál función es continua en todo $\\mathbb{R}$?",
        "respuestas": {"A": "$\\tan x$", "B": "$\\frac{1}{x}$", "C": "$x^3-2x+1$", "D": "$\\sqrt{x}$"}
    },

    # =========================================================================
    # TEMA 16: La derivada
    # =========================================================================
    "MOCK-0223": {
        "pregunta": "La derivada de $f$ en $a$ se define formalmente como:",
        "respuestas": {
            "A": "$\\lim_{h \\to 0} \\frac{f(a+h)-f(a)}{h}$",
            "B": "$\\frac{f(a)}{a}$",
            "C": "$\\lim_{x \\to a} f(x)$",
            "D": "$\\int f(x)\\,dx$"
        }
    },
    "MOCK-0224": {
        "pregunta": "Otra notación usual para la derivada de $y$ respecto de $x$ es:",
        "respuestas": {"A": "$\\frac{dy}{dx}$", "B": "$\\frac{dx}{dy}$", "C": "$\\int y\\,dx$", "D": "$\\frac{\\Delta x}{\\Delta y}$"}
    },
    "MOCK-0225": {
        "pregunta": "Si $f(x) = |x|$, la función $f$ no es derivable en:",
        "respuestas": {"A": "$x = -1$", "B": "$x = 0$", "C": "$x = 1$", "D": "$x = 2$"}
    },
    "MOCK-0226": {
        "pregunta": "Deriva: $f(x) = 4x^3-2x$.",
        "respuestas": {"A": "$12x^2-2$", "B": "$4x^2-2$", "C": "$12x-2$", "D": "$x^4-x^2$"}
    },
    "MOCK-0227": {
        "pregunta": "Deriva: $f(x) = \\sqrt{x}$.",
        "respuestas": {"A": "$\\frac{\\sqrt{x}}{2}$", "B": "$\\frac{1}{2\\sqrt{x}}$", "C": "$2\\sqrt{x}$", "D": "$\\frac{1}{\\sqrt{x}}$"}
    },
    "MOCK-0228": {
        "pregunta": "Deriva: $f(x) = \\frac{5}{x}$.",
        "respuestas": {"A": "$\\frac{5}{x^2}$", "B": "$-\\frac{5}{x^2}$", "C": "$-\\frac{x^2}{5}$", "D": "$5\\ln x$"}
    },
    "MOCK-0229": {
        "pregunta": "Deriva: $(3x+1)^5$.",
        "respuestas": {"A": "$5(3x+1)^4$", "B": "$15(3x+1)^4$", "C": "$15(3x+1)^5$", "D": "$3(3x+1)^4$"}
    },
    "MOCK-0230": {
        "pregunta": "Deriva: $\\operatorname{sen}(x^2)$.",
        "respuestas": {"A": "$\\cos(x^2)$", "B": "$2x \\cos(x^2)$", "C": "$-2x \\operatorname{sen}(x^2)$", "D": "$2x \\operatorname{sen}(x^2)$"}
    },
    "MOCK-0231": {
        "pregunta": "Deriva: $\\ln(2x+3)$.",
        "respuestas": {"A": "$\\frac{1}{2x+3}$", "B": "$\\frac{2}{2x+3}$", "C": "$\\ln 2$", "D": "$\\frac{2x}{2x+3}$"}
    },
    "MOCK-0232": {
        "pregunta": "Si $x^2+y^2=25$, entonces $\\frac{dy}{dx} =$",
        "respuestas": {"A": "$\\frac{x}{y}$", "B": "$-\\frac{x}{y}$", "C": "$-\\frac{y}{x}$", "D": "$2x+2y$"}
    },
    "MOCK-0233": {
        "pregunta": "Si $xy = 6$, entonces $\\frac{dy}{dx} =$",
        "respuestas": {"A": "$\\frac{y}{x}$", "B": "$-\\frac{y}{x}$", "C": "$-\\frac{x}{y}$", "D": "$\\frac{1}{xy}$"}
    },
    "MOCK-0234": {
        "pregunta": "Si $x^2+xy+y^2=7$, entonces $\\frac{dy}{dx} =$",
        "respuestas": {"A": "$-\\frac{2x+y}{x+2y}$", "B": "$\\frac{2x+y}{x+2y}$", "C": "$-\\frac{x+2y}{2x+y}$", "D": "$-\\frac{2x}{y}$"}
    },
    "MOCK-0235": {
        "pregunta": "Si $f(x) = x^4$, entonces $f''(x) =$",
        "respuestas": {"A": "$4x^3$", "B": "$12x^2$", "C": "$24x$", "D": "$24$"}
    },
    "MOCK-0236": {
        "pregunta": "La tercera derivada de $f(x) = x^3$ es:",
        "respuestas": {"A": "$3x^2$", "B": "$6x$", "C": "$6$", "D": "$0$"}
    },
    "MOCK-0237": {
        "pregunta": "Si $f(x) = e^x$, entonces $f^{(4)}(x) =$",
        "respuestas": {"A": "$4e^x$", "B": "$e^x$", "C": "$-e^x$", "D": "$0$"}
    },
    "MOCK-0238": {
        "pregunta": "Geométricamente, $f'(a)$ representa:",
        "respuestas": {"A": "Área bajo la curva", "B": "Pendiente de la recta tangente", "C": "Ordenada al origen", "D": "Longitud de arco"}
    },
    "MOCK-0239": {
        "pregunta": "Si $f'(x) < 0$ en un intervalo, la función $f$ es:",
        "respuestas": {"A": "Creciente", "B": "Decreciente", "C": "Constante", "D": "Discontinua"}
    },
    "MOCK-0240": {
        "pregunta": "Físicamente, si $s(t)$ representa la posición, $s'(t)$ representa la:",
        "respuestas": {"A": "Aceleración", "B": "Velocidad", "C": "Distancia total", "D": "Tiempo"}
    },
    "MOCK-0241": {
        "pregunta": "Ecuación de la recta tangente a $y = x^2$ en $x=1$:",
        "respuestas": {"A": "$y = 2x-1$", "B": "$y = x+1$", "C": "$y = -2x+3$", "D": "$y = 2x+1$"}
    },
    "MOCK-0242": {
        "pregunta": "La pendiente de la recta normal a una curva cuya tangente tiene pendiente $3$ es:",
        "respuestas": {"A": "$3$", "B": "$-3$", "C": "$1/3$", "D": "$-1/3$"}
    },
    "MOCK-0243": {
        "pregunta": "Recta normal a $y = x^2$ en el punto $(0,0)$:",
        "respuestas": {"A": "$y = 0$", "B": "$x = 0$", "C": "$y = x$", "D": "$y = -x$"}
    },
    "MOCK-0244": {
        "pregunta": "Si la posición es $s(t) = t^3-3t$, la velocidad en $t=2$ es:",
        "respuestas": {"A": "$3$", "B": "$6$", "C": "$9$", "D": "$12$"}
    },
    "MOCK-0245": {
        "pregunta": "Si $s(t) = 4t^2+2t$, la aceleración es:",
        "respuestas": {"A": "$4t+2$", "B": "$8t+2$", "C": "$8$", "D": "$4$"}
    },
    "MOCK-0246": {
        "pregunta": "Si la velocidad es $v(t) = 5t-1$, la aceleración es:",
        "respuestas": {"A": "$5t$", "B": "$5$", "C": "$-1$", "D": "$0$"}
    },
    "MOCK-0247": {
        "pregunta": "Los puntos críticos de $f(x) = x^2-4x+1$ incluyen:",
        "respuestas": {"A": "$x = 0$", "B": "$x = 1$", "C": "$x = 2$", "D": "$x = 4$"}
    },
    "MOCK-0248": {
        "pregunta": "La función $f(x) = -x^2+6x$ tiene un máximo relativo en:",
        "respuestas": {"A": "$x = -3$", "B": "$x = 0$", "C": "$x = 3$", "D": "$x = 6$"}
    },
    "MOCK-0249": {
        "pregunta": "Si $f'$ cambia de signo negativo a positivo al pasar por $c$, $f$ tiene en $c$ un:",
        "respuestas": {"A": "Máximo relativo", "B": "Mínimo relativo", "C": "Punto discontinuo", "D": "Punto sin derivada"}
    },
    "MOCK-0250": {
        "pregunta": "El valor máximo absoluto de $f(x) = x$ en $[0,5]$ es:",
        "respuestas": {"A": "$0$", "B": "$1$", "C": "$5$", "D": "No existe"}
    },
    "MOCK-0251": {
        "pregunta": "El valor mínimo absoluto de $f(x) = x^2$ en $[-2,3]$ es:",
        "respuestas": {"A": "$-2$", "B": "$0$", "C": "$4$", "D": "$9$"}
    },
    "MOCK-0252": {
        "pregunta": "Para hallar extremos absolutos en $[a,b]$ se evalúan:",
        "respuestas": {"A": "Solo puntos críticos", "B": "Solo los extremos del intervalo", "C": "Puntos críticos y extremos del intervalo", "D": "Todos los números reales"}
    },
    "MOCK-0253": {
        "pregunta": "El punto de inflexión de $f(x) = x^3$ ocurre en:",
        "respuestas": {"A": "$x = -1$", "B": "$x = 0$", "C": "$x = 1$", "D": "$x = 3$"}
    },
    "MOCK-0254": {
        "pregunta": "Si $f''(x) > 0$ en un intervalo, la gráfica es:",
        "respuestas": {"A": "Cóncava hacia arriba", "B": "Cóncava hacia abajo", "C": "Decreciente siempre", "D": "Discontinua"}
    },
    "MOCK-0255": {
        "pregunta": "Para $f(x) = x^3-3x^2$, la abscisa de inflexión es:",
        "respuestas": {"A": "$x = 0$", "B": "$x = 1$", "C": "$x = 2$", "D": "$x = 3$"}
    },
    "MOCK-0256": {
        "pregunta": "Un rectángulo tiene perímetro $20$. ¿Qué dimensiones maximizan el área?",
        "respuestas": {"A": "$1$ y $9$", "B": "$2$ y $8$", "C": "$5$ y $5$", "D": "$4$ y $6$"}
    },
    "MOCK-0257": {
        "pregunta": "La altura de un proyectil es $h(t) = -5t^2+20t+1$. ¿Cuándo alcanza su altura máxima?",
        "respuestas": {"A": "$1\\text{ s}$", "B": "$2\\text{ s}$", "C": "$4\\text{ s}$", "D": "$5\\text{ s}$"}
    },
    "MOCK-0258": {
        "pregunta": "Una caja sin tapa se forma cortando cuadrados de lado $x$ de una lámina de $12 \\times 12$. Su volumen es:",
        "respuestas": {"A": "$x(12-2x)^2$", "B": "$x^2(12-x)$", "C": "$12x^2$", "D": "$(12-x)^3$"}
    },

    # =========================================================================
    # TEMA 17: La integral
    # =========================================================================
    "MOCK-0259": {
        "pregunta": "¿Cuál función es integrable en $[0,1]$?",
        "respuestas": {
            "A": "$f(x) = x^2$",
            "B": "$f(x) = \\frac{1}{x}$ con $f(0)$ no definida",
            "C": "Una función no acotada",
            "D": "Una función con infinitas oscilaciones no acotadas"
        }
    },
    "MOCK-0260": {
        "pregunta": "Toda función continua en un intervalo cerrado $[a,b]$ es:",
        "respuestas": {"A": "No integrable", "B": "Integrable", "C": "Constante", "D": "Derivable siempre"}
    },
    "MOCK-0261": {
        "pregunta": "Una función acotada con un número finito de discontinuidades en $[a,b]$ es:",
        "respuestas": {"A": "Integrable", "B": "Siempre derivable", "C": "No acotada", "D": "Periódica"}
    },
    "MOCK-0262": {
        "pregunta": "Si $\\int_a^b f = 3$ y $\\int_a^b g = 2$, entonces $\\int_a^b (f+g) =$",
        "respuestas": {"A": "$1$", "B": "$5$", "C": "$6$", "D": "$\\frac{3}{2}$"}
    },
    "MOCK-0263": {
        "pregunta": "La propiedad $\\int [c f(x)]\\,dx = c \\int f(x)\\,dx$ se conoce como:",
        "respuestas": {"A": "Linealidad", "B": "Periodicidad", "C": "Concavidad", "D": "Derivabilidad"}
    },
    "MOCK-0264": {
        "pregunta": "Si $\\int_a^b f(x)\\,dx = 7$, entonces $\\int_b^a f(x)\\,dx =$",
        "respuestas": {"A": "$7$", "B": "$-7$", "C": "$0$", "D": "$14$"}
    },
    "MOCK-0265": {
        "pregunta": "Integra: $\\int x^3\\,dx$.",
        "respuestas": {"A": "$\\frac{x^4}{4}+C$", "B": "$3x^2+C$", "C": "$x^4+C$", "D": "$\\frac{x^2}{2}+C$"}
    },
    "MOCK-0266": {
        "pregunta": "Integra: $\\int 5\\,dx$.",
        "respuestas": {"A": "$5x+C$", "B": "$x^5+C$", "C": "$5+C$", "D": "$\\ln 5+C$"}
    },
    "MOCK-0267": {
        "pregunta": "Integra: $\\int \\frac{1}{x}\\,dx$.",
        "respuestas": {"A": "$\\frac{1}{x^2}+C$", "B": "$\\ln|x|+C$", "C": "$x\\ln x+C$", "D": "$e^x+C$"}
    },
    "MOCK-0268": {
        "pregunta": "Integra: $\\int \\cos(3x)\\,dx$.",
        "respuestas": {"A": "$\\operatorname{sen}(3x)+C$", "B": "$\\frac{1}{3}\\operatorname{sen}(3x)+C$", "C": "$-3\\operatorname{sen} x+C$", "D": "$3\\operatorname{sen}(3x)+C$"}
    },
    "MOCK-0269": {
        "pregunta": "Integra: $\\int e^{2x}\\,dx$.",
        "respuestas": {"A": "$2e^{2x}+C$", "B": "$\\frac{1}{2}e^{2x}+C$", "C": "$e^x+C$", "D": "$e^{2x}+C$"}
    },
    "MOCK-0270": {
        "pregunta": "Integra: $\\int \\sec^2 x\\,dx$.",
        "respuestas": {"A": "$\\sec x+C$", "B": "$\\tan x+C$", "C": "$-\\cot x+C$", "D": "$\\operatorname{sen} x+C$"}
    },
    "MOCK-0271": {
        "pregunta": "Para $\\int 2x \\cos(x^2)\\,dx$, una sustitución conveniente es:",
        "respuestas": {"A": "$u = 2x$", "B": "$u = x^2$", "C": "$u = \\cos x$", "D": "$u = x+2$"}
    },
    "MOCK-0272": {
        "pregunta": "Integra por partes: $\\int x e^x\\,dx$.",
        "respuestas": {"A": "$xe^x - e^x + C$", "B": "$xe^x + e^x + C$", "C": "$e^x + C$", "D": "$\\frac{x^2 e^x}{2} + C$"}
    },
    "MOCK-0273": {
        "pregunta": "Integra: $\\int \\frac{dx}{x^2-1}$ por fracciones parciales. Una descomposición correcta es:",
        "respuestas": {"A": "$\\frac{1}{2}\\left[\\frac{1}{x-1} - \\frac{1}{x+1}\\right]$", "B": "$\\frac{1}{x-1} + \\frac{1}{x+1}$", "C": "$\\frac{1}{2}\\left[\\frac{1}{x-1} + \\frac{1}{x+1}\\right]$", "D": "$\\frac{1}{x^2-1}$"}
    },
    "MOCK-0274": {
        "pregunta": "Calcula: $\\int_0^2 x\\,dx$.",
        "respuestas": {"A": "$1$", "B": "$2$", "C": "$3$", "D": "$4$"}
    },
    "MOCK-0275": {
        "pregunta": "Si $F'=f$, entonces $\\int_a^b f(x)\\,dx =$",
        "respuestas": {"A": "$F(a)+F(b)$", "B": "$F(b)-F(a)$", "C": "$F(a)-F(b)$", "D": "$f(b)-f(a)$"}
    },
    "MOCK-0276": {
        "pregunta": "Calcula: $\\int_1^3 2\\,dx$.",
        "respuestas": {"A": "$2$", "B": "$4$", "C": "$6$", "D": "$8$"}
    }
}

def aplicar_transformaciones():
    archivo_origen = Path("assets/reactivos.json.bak")
    archivo_destino = Path("assets/reactivos.json")
    
    data = json.loads(archivo_origen.read_text(encoding="utf-8"))
    reactivos = data["reactivos"]
    
    total = len(reactivos)
    modificados = 0
    
    for r in reactivos:
        r_id = r["id"]
        if r_id in REACTIVOS_LATEX:
            item = REACTIVOS_LATEX[r_id]
            r["pregunta"] = item["pregunta"]
            # Preservar las claves A, B, C, D exactamente
            for letra, texto in item["respuestas"].items():
                r["respuestas_posibles"][letra] = texto
            modificados += 1
        else:
            print(f"ADVERTENCIA: {r_id} no encontrado en REACTIVOS_LATEX")
            
    print(f"Reactivos modificados con LaTeX: {modificados} de {total}")
    
    # Escribir con formato bonito e indentado
    archivo_destino.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("assets/reactivos.json guardado con éxito.")

if __name__ == "__main__":
    aplicar_transformaciones()
