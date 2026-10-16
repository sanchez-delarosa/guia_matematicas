"""
Iconos vectoriales minimalistas estilo Brilliant.org con la paleta Axler de la guía.
Cada icono está diseñado en un viewBox de 0 0 100 100 con trazos limpios,
esquinas redondeadas y semántica matemática visual.
"""

from __future__ import annotations

# Paleta oficial:
# Marino: #1B2A4A, Ámbar: #E8B400, Terracota: #D99884
# Marino Borde/Pastel: #8FA3C4, #E4EAF4
# Ámbar Borde/Pastel: #F2D98A, #FFF6D9

ICONOS_PARTES: dict[str, str] = {
    # 1. Aritmética
    "Parte I: Aritmética": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.12"/>
  <!-- Bloque izquierdo (Terracota) -->
  <path d="M18 56L28 51L38 56L28 61Z" fill="#FBEAE5"/>
  <rect x="18" y="56" width="20" height="22" rx="4" fill="#D99884"/>
  <line x1="23" y1="67" x2="33" y2="67" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Bloque central doble (Ámbar + Marino) -->
  <path d="M50 35L62 29V74L50 80Z" fill="#1B2A4A"/>
  <path d="M38 35L50 29L62 35L50 41Z" fill="#FFF6D9"/>
  <rect x="38" y="57" width="24" height="22" rx="4" fill="#E8B400"/>
  <rect x="38" y="35" width="24" height="20" rx="4" fill="#E8B400"/>
  <line x1="38" y1="56" x2="62" y2="56" stroke="#1B2A4A" stroke-width="1.8"/>
  <!-- Bloque derecho (Marino) -->
  <path d="M72 44L82 39V68L72 73Z" fill="#141E34"/>
  <path d="M64 44L74 39L82 44L72 49Z" fill="#8FA3C4"/>
  <rect x="64" y="44" width="18" height="28" rx="4" fill="#1B2A4A"/>
  <path d="M69 53L77 61M77 53L69 61" stroke="#E8B400" stroke-width="2.4" stroke-linecap="round"/>
  <!-- Signo '+' flotante -->
  <path d="M31 24V34M26 29H36" stroke="#1B2A4A" stroke-width="2.8" stroke-linecap="round"/>
  <circle cx="76" cy="27" r="3" fill="#E8B400"/>
</svg>""",

    # 2. Álgebra
    "Parte II: Álgebra": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <!-- Ejes coordenados -->
  <line x1="20" y1="50" x2="80" y2="50" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.6"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.6"/>
  <!-- Soporte central -->
  <path d="M42 76C42 73 46 71 50 71C54 71 58 73 58 76H42Z" fill="#1B2A4A"/>
  <rect x="48" y="50" width="4" height="22" rx="2" fill="#1B2A4A"/>
  <circle cx="50" cy="50" r="3" fill="#E8B400"/>
  <!-- Barra de la balanza -->
  <rect x="18" y="48.5" width="64" height="3.5" rx="1.75" fill="#1B2A4A"/>
  <!-- Plato izquierdo (Incógnita X) -->
  <path d="M22 52L26 62H38L42 52" stroke="#1B2A4A" stroke-width="1.5" stroke-linecap="round" fill="none"/>
  <rect x="25" y="37" width="20" height="20" rx="4" fill="#1B2A4A"/>
  <path d="M30 42L40 52M40 42L30 52" stroke="#E8B400" stroke-width="2.6" stroke-linecap="round"/>
  <!-- Plato derecho (Pesos) -->
  <path d="M58 52L62 62H74L78 52" stroke="#1B2A4A" stroke-width="1.5" stroke-linecap="round" fill="none"/>
  <rect x="63" y="44" width="13" height="13" rx="3" fill="#D99884"/>
  <rect x="68" y="30" width="13" height="13" rx="3" fill="#E8B400"/>
</svg>""",

    # 3. Funciones
    "Parte III: Funciones": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#8FA3C4" fill-opacity="0.12"/>
  <!-- Ejes -->
  <path d="M18 78H82M24 18V82" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Curva cúbica sigmoide f(x) -->
  <path d="M24 72C36 72 40 54 52 46C64 38 70 24 82 22" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <!-- Líneas punteadas de mapeo (x, f(x)) -->
  <line x1="52" y1="46" x2="52" y2="78" stroke="#8FA3C4" stroke-width="1.5" stroke-dasharray="2 2"/>
  <line x1="24" y1="46" x2="52" y2="46" stroke="#8FA3C4" stroke-width="1.5" stroke-dasharray="2 2"/>
  <!-- Puntos del dominio y contradominio -->
  <circle cx="52" cy="78" r="2.5" fill="#D99884"/>
  <circle cx="24" cy="46" r="2.5" fill="#D99884"/>
  <!-- Punto en la curva -->
  <circle cx="52" cy="46" r="4.5" fill="#E8B400"/>
  <circle cx="52" cy="46" r="2" fill="#1B2A4A"/>
</svg>""",

    # 4. Geometría euclidiana
    "Parte IV: Geometría euclidiana": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#D99884" fill-opacity="0.1"/>
  <!-- Triángulo rectángulo principal -->
  <path d="M22 76L78 76L78 30Z" fill="#E4EAF4" stroke="#1B2A4A" stroke-width="2.5" stroke-linejoin="round"/>
  <!-- Ángulo recto -->
  <path d="M68 76V66H78" stroke="#E8B400" stroke-width="2" stroke-linecap="round"/>
  <!-- Arco de ángulo agudo -->
  <path d="M36 76C36 72 34 68 31 66" stroke="#D99884" stroke-width="2" stroke-linecap="round"/>
  <!-- Cuadrado auxiliar sobre cateto menor -->
  <rect x="78" y="30" width="12" height="46" rx="2" fill="#FFF6D9" stroke="#E8B400" stroke-width="1.2"/>
  <!-- Vértices destacados -->
  <circle cx="22" cy="76" r="3.2" fill="#1B2A4A"/>
  <circle cx="78" cy="76" r="3.2" fill="#1B2A4A"/>
  <circle cx="78" cy="30" r="3.2" fill="#E8B400"/>
</svg>""",

    # 5. Trigonometría
    "Parte V: Trigonometría": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.1"/>
  <!-- Ejes del círculo unitario -->
  <line x1="14" y1="50" x2="86" y2="50" stroke="#8FA3C4" stroke-width="1.2"/>
  <line x1="50" y1="14" x2="50" y2="86" stroke="#8FA3C4" stroke-width="1.2"/>
  <!-- Círculo unitario -->
  <circle cx="50" cy="50" r="30" stroke="#1B2A4A" stroke-width="2"/>
  <!-- Triángulo rectángulo trigonométrico -->
  <path d="M50 50L72 32V50Z" fill="#FFF6D9" stroke="#1B2A4A" stroke-width="1.8" stroke-linejoin="round"/>
  <!-- Radio vector en dorado -->
  <line x1="50" y1="50" x2="72" y2="32" stroke="#E8B400" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Arco de ángulo theta -->
  <path d="M58 50C58 47 56 45 54 44" stroke="#D99884" stroke-width="2" stroke-linecap="round"/>
  <!-- Proyección sen y cos -->
  <line x1="72" y1="32" x2="72" y2="50" stroke="#D99884" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="50" y1="50" x2="72" y2="50" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="2.5" fill="#1B2A4A"/>
  <circle cx="72" cy="32" r="3" fill="#E8B400"/>
</svg>""",

    # 6. Geometría analítica
    "Parte VI: Geometría analítica": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <!-- Cuadrícula sutil -->
  <path d="M20 30H80M20 50H80M20 70H80M30 20V80M50 20V80M70 20V80" stroke="#8FA3C4" stroke-width="0.8" opacity="0.4"/>
  <!-- Ejes -->
  <line x1="15" y1="50" x2="85" y2="50" stroke="#1B2A4A" stroke-width="1.8"/>
  <line x1="50" y1="15" x2="50" y2="85" stroke="#1B2A4A" stroke-width="1.8"/>
  <!-- Parábola en azul marino -->
  <path d="M26 22C38 68 62 68 74 22" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <!-- Recta directriz punteada -->
  <line x1="22" y1="72" x2="78" y2="72" stroke="#D99884" stroke-width="1.8" stroke-dasharray="3 3"/>
  <!-- Vértice y Foco -->
  <circle cx="50" cy="56" r="3" fill="#E8B400"/>
  <circle cx="50" cy="42" r="3" fill="#D99884"/>
</svg>""",

    # 7. Cálculo diferencial
    "Parte VII: Cálculo diferencial": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#FBEAE5" fill-opacity="0.6"/>
  <!-- Ejes -->
  <path d="M16 78H84M22 16V84" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Curva continua con máximo y mínimo -->
  <path d="M22 66C32 40 42 28 54 36C66 44 72 60 84 20" stroke="#1B2A4A" stroke-width="3.2" stroke-linecap="round"/>
  <!-- Recta tangente en el punto de inflexión/pendiente -->
  <line x1="44" y1="62" x2="80" y2="24" stroke="#1B2A4A" stroke-width="2.6" stroke-linecap="round"/>
  <line x1="44" y1="62" x2="80" y2="24" stroke="#E8B400" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Triángulo pendiente dy/dx -->
  <path d="M56 49H66V39" stroke="#D99884" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Punto de tangencia -->
  <circle cx="62" cy="43" r="3.5" fill="#E8B400"/>
  <circle cx="62" cy="43" r="1.5" fill="#1B2A4A"/>
</svg>""",

    # 8. Cálculo integral
    "Parte VIII: Cálculo integral": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E4EAF4" fill-opacity="0.6"/>
  <!-- Ejes -->
  <path d="M14 74H86M20 14V80" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Rectángulos de Riemann (Área) -->
  <rect x="25" y="46" width="9" height="28" rx="1.5" fill="#D99884"/>
  <rect x="35" y="34" width="9" height="40" rx="1.5" fill="#E8B400"/>
  <rect x="45" y="28" width="9" height="46" rx="1.5" fill="#E8B400"/>
  <rect x="55" y="36" width="9" height="38" rx="1.5" fill="#8FA3C4"/>
  <rect x="65" y="48" width="9" height="26" rx="1.5" fill="#8FA3C4"/>
  <!-- Curva integral f(x) -->
  <path d="M20 62C28 44 38 24 50 26C62 28 68 56 82 44" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <!-- Signo integral sutil decorativo -->
  <path d="M83 24C83 20 80 18 78 18C75 18 75 22 75 26V34" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round" fill="none"/>
</svg>""",

    # 9. Probabilidad y estadística
    "Parte IX: Probabilidad y estadística": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.1"/>
  <!-- Eje horizontal -->
  <line x1="14" y1="76" x2="86" y2="76" stroke="#1B2A4A" stroke-width="1.8"/>
  <!-- Campana de Gauss (Distribución normal) -->
  <path d="M18 76C28 76 36 74 42 50C46 34 48 24 50 24C52 24 54 34 58 50C64 74 72 76 82 76"
        fill="#FFF6D9" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Área de desviación típica central (1 sigma) -->
  <rect x="44" y="38" width="12" height="38" fill="#E8B400" fill-opacity="0.35"/>
  <line x1="50" y1="24" x2="50" y2="76" stroke="#D99884" stroke-width="1.8" stroke-dasharray="2 2"/>
  <!-- Dado o símbolo aleatorio -->
  <rect x="68" y="24" width="16" height="16" rx="3.5" fill="#1B2A4A"/>
  <circle cx="72" cy="28" r="1.2" fill="white"/>
  <circle cx="76" cy="32" r="1.2" fill="white"/>
  <circle cx="80" cy="36" r="1.2" fill="white"/>
</svg>""",

    # 10. Razonamiento matemático
    "Parte X: Razonamiento matemático": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#D99884" fill-opacity="0.12"/>
  <!-- Patrón secuencial geométrico (Cubo dentro de hexágono / engrane) -->
  <path d="M50 20L78 36V68L50 84L22 68V36L50 20Z" fill="#E4EAF4" stroke="#1B2A4A" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M50 20V52L78 68M50 52L22 68" stroke="#1B2A4A" stroke-width="2.2" stroke-linejoin="round"/>
  <!-- Resalte de una cara isométrica (Ámbar) -->
  <path d="M50 20L78 36L50 52L22 36Z" fill="#E8B400" fill-opacity="0.75"/>
  <!-- Pieza complementaria (Terracota) -->
  <path d="M22 36L50 52V84L22 68Z" fill="#D99884" fill-opacity="0.85"/>
  <!-- Foco / Destello de deducción -->
  <circle cx="50" cy="52" r="4" fill="#1B2A4A"/>
  <circle cx="50" cy="52" r="2" fill="#FFF6D9"/>
</svg>""",

    # 11. Matemáticas financieras
    "Parte XI: Matemáticas financieras": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.12"/>
  <!-- Ejes -->
  <path d="M16 76H84M22 18V80" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <!-- Columnas de crecimiento compuesto -->
  <rect x="28" y="60" width="10" height="16" rx="2" fill="#8FA3C4"/>
  <rect x="42" y="48" width="10" height="28" rx="2" fill="#D99884"/>
  <rect x="56" y="34" width="10" height="42" rx="2" fill="#E8B400"/>
  <!-- Curva exponencial con flecha ascendente -->
  <path d="M26 62C38 60 52 46 72 26" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <path d="M64 24L74 24L74 34" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Símbolo de porcentaje '%' -->
  <circle cx="76" cy="46" r="2.2" fill="#1B2A4A"/>
  <circle cx="84" cy="56" r="2.2" fill="#1B2A4A"/>
  <line x1="85" y1="45" x2="75" y2="57" stroke="#E8B400" stroke-width="2" stroke-linecap="round"/>
</svg>"""
}


def obtener_icono_parte(nombre_parte: str) -> str:
    """Devuelve el SVG correspondiente a la parte, o uno genérico si no coincide."""
    for clave, svg in ICONOS_PARTES.items():
        if clave in nombre_parte or nombre_parte in clave:
            return svg
    # Icono genérico matemático por defecto (cubo / compás)
    return ICONOS_PARTES["Parte I: Aritmética"]


ICONOS_TEMAS_PRACTICA: dict[str, str] = {
    # 1. Reales, complejos y expresiones
    "1": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.12"/>
  <rect x="20" y="52" width="22" height="24" rx="4" fill="#D99884"/>
  <line x1="26" y1="64" x2="36" y2="64" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="44" y="36" width="24" height="40" rx="4" fill="#E8B400"/>
  <line x1="56" y1="44" x2="56" y2="68" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="48" y1="56" x2="64" y2="56" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="70" y="44" width="16" height="32" rx="4" fill="#1B2A4A"/>
  <circle cx="78" cy="52" r="2.5" fill="#E8B400"/>
  <line x1="78" y1="58" x2="78" y2="68" stroke="#E8B400" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="32" cy="30" r="3" fill="#D99884"/>
</svg>""",

    # 2. Productos notables y factorización
    "2": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <rect x="22" y="22" width="34" height="34" rx="3" fill="#1B2A4A"/>
  <rect x="58" y="22" width="20" height="34" rx="3" fill="#D99884"/>
  <rect x="22" y="58" width="34" height="20" rx="3" fill="#D99884"/>
  <rect x="58" y="58" width="20" height="20" rx="3" fill="#E8B400"/>
  <path d="M39 39L58 58" stroke="#FFF6D9" stroke-width="2" stroke-dasharray="2 2"/>
</svg>""",

    # 3. Ecuaciones
    "3": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#8FA3C4" fill-opacity="0.14"/>
  <rect x="47" y="42" width="6" height="36" rx="3" fill="#1B2A4A"/>
  <path d="M38 78H62" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <circle cx="50" cy="42" r="5" fill="#E8B400"/>
  <rect x="18" y="40" width="64" height="4" rx="2" fill="#1B2A4A"/>
  <path d="M22 44L26 56H38L42 44" stroke="#1B2A4A" stroke-width="1.8" fill="none"/>
  <rect x="26" y="32" width="12" height="12" rx="3" fill="#D99884"/>
  <path d="M58 44L62 56H74L78 44" stroke="#1B2A4A" stroke-width="1.8" fill="none"/>
  <rect x="62" y="32" width="12" height="12" rx="3" fill="#1B2A4A"/>
</svg>""",

    # 4. Desigualdades
    "4": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#D99884" fill-opacity="0.12"/>
  <line x1="16" y1="52" x2="84" y2="52" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="32" y1="52" x2="68" y2="52" stroke="#E8B400" stroke-width="5" stroke-linecap="round"/>
  <circle cx="32" cy="52" r="6" fill="#1B2A4A"/>
  <circle cx="32" cy="52" r="3" fill="#FFF6D9"/>
  <circle cx="68" cy="52" r="6" fill="#D99884" stroke="#1B2A4A" stroke-width="2.5"/>
  <path d="M44 30L56 36L44 42" stroke="#1B2A4A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    # 5. Sistemas de ecuaciones
    "5": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <line x1="20" y1="50" x2="80" y2="50" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <line x1="22" y1="74" x2="78" y2="26" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <line x1="22" y1="32" x2="78" y2="68" stroke="#D99884" stroke-width="3" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="6" fill="#E8B400" stroke="#1B2A4A" stroke-width="2"/>
</svg>""",

    # 6. Funciones algebraicas
    "6": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#8FA3C4" fill-opacity="0.12"/>
  <path d="M18 78H82M24 18V82" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M24 72C36 72 40 54 52 46C64 38 70 24 82 22" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <line x1="52" y1="46" x2="52" y2="78" stroke="#8FA3C4" stroke-width="1.5" stroke-dasharray="2 2"/>
  <line x1="24" y1="46" x2="52" y2="46" stroke="#8FA3C4" stroke-width="1.5" stroke-dasharray="2 2"/>
  <circle cx="52" cy="78" r="2.5" fill="#D99884"/>
  <circle cx="24" cy="46" r="2.5" fill="#D99884"/>
  <circle cx="52" cy="46" r="4.5" fill="#E8B400"/>
</svg>""",

    # 7. Trigonometría
    "7": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.1"/>
  <line x1="14" y1="50" x2="86" y2="50" stroke="#8FA3C4" stroke-width="1.2"/>
  <line x1="50" y1="14" x2="50" y2="86" stroke="#8FA3C4" stroke-width="1.2"/>
  <circle cx="50" cy="50" r="30" stroke="#1B2A4A" stroke-width="2"/>
  <path d="M50 50L72 32V50Z" fill="#FFF6D9" stroke="#1B2A4A" stroke-width="1.8" stroke-linejoin="round"/>
  <line x1="50" y1="50" x2="72" y2="32" stroke="#E8B400" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M58 50C58 47 56 45 54 44" stroke="#D99884" stroke-width="2" stroke-linecap="round"/>
  <line x1="72" y1="32" x2="72" y2="50" stroke="#D99884" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="50" y1="50" x2="72" y2="50" stroke="#1B2A4A" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="72" cy="32" r="3" fill="#E8B400"/>
</svg>""",

    # 8. Funciones exponenciales y logarítmicas
    "8": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#D99884" fill-opacity="0.12"/>
  <path d="M16 80H84M22 16V84" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="22" y1="72" x2="82" y2="72" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <path d="M22 71C40 70 54 62 66 42C74 28 78 18 80 16" stroke="#1B2A4A" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="54" cy="62" r="4" fill="#E8B400"/>
  <circle cx="54" cy="62" r="2" fill="#1B2A4A"/>
</svg>""",

    # 9. Recta
    "9": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <line x1="16" y1="78" x2="84" y2="78" stroke="#8FA3C4" stroke-width="1.5"/>
  <line x1="22" y1="16" x2="22" y2="84" stroke="#8FA3C4" stroke-width="1.5"/>
  <line x1="20" y1="72" x2="80" y2="28" stroke="#1B2A4A" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M42 56H64V40" stroke="#D99884" stroke-width="2" stroke-linecap="round"/>
  <circle cx="42" cy="56" r="4" fill="#E8B400"/>
  <circle cx="64" cy="40" r="4" fill="#E8B400"/>
</svg>""",

    # 10. Circunferencia
    "10": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.12"/>
  <line x1="20" y1="50" x2="80" y2="50" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <circle cx="50" cy="50" r="28" stroke="#1B2A4A" stroke-width="3"/>
  <circle cx="50" cy="50" r="3.5" fill="#1B2A4A"/>
  <line x1="50" y1="50" x2="70" y2="30" stroke="#D99884" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="70" cy="30" r="4" fill="#E8B400"/>
</svg>""",

    # 11. Parábola
    "11": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <line x1="15" y1="50" x2="85" y2="50" stroke="#8FA3C4" stroke-width="1.2"/>
  <line x1="50" y1="15" x2="50" y2="85" stroke="#8FA3C4" stroke-width="1.2"/>
  <path d="M26 24C38 70 62 70 74 24" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <line x1="22" y1="74" x2="78" y2="74" stroke="#D99884" stroke-width="1.8" stroke-dasharray="3 3"/>
  <circle cx="50" cy="58" r="3.5" fill="#E8B400"/>
  <circle cx="50" cy="42" r="3.5" fill="#D99884"/>
</svg>""",

    # 12. Elipse
    "12": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#D99884" fill-opacity="0.12"/>
  <line x1="14" y1="50" x2="86" y2="50" stroke="#8FA3C4" stroke-width="1.2"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#8FA3C4" stroke-width="1.2"/>
  <ellipse cx="50" cy="50" rx="34" ry="20" stroke="#1B2A4A" stroke-width="3"/>
  <circle cx="34" cy="50" r="3.5" fill="#E8B400"/>
  <circle cx="66" cy="50" r="3.5" fill="#E8B400"/>
  <circle cx="50" cy="50" r="2.5" fill="#1B2A4A"/>
</svg>""",

    # 13. Hipérbola
    "13": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#1B2A4A" fill-opacity="0.08"/>
  <line x1="22" y1="22" x2="78" y2="78" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <line x1="22" y1="78" x2="78" y2="22" stroke="#8FA3C4" stroke-width="1.2" stroke-dasharray="2 2"/>
  <path d="M22 26C36 38 36 62 22 74" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <path d="M78 26C64 38 64 62 78 74" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <circle cx="33" cy="50" r="3.5" fill="#E8B400"/>
  <circle cx="67" cy="50" r="3.5" fill="#E8B400"/>
</svg>""",

    # 14. Ecuación general de segundo grado
    "14": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E8B400" fill-opacity="0.12"/>
  <path d="M28 24L72 24L50 50L28 24Z" fill="#FFF6D9" stroke="#1B2A4A" stroke-width="2" stroke-linejoin="round"/>
  <path d="M50 50L72 76L28 76L50 50Z" fill="#FBEAE5" stroke="#1B2A4A" stroke-width="2" stroke-linejoin="round"/>
  <line x1="20" y1="36" x2="80" y2="58" stroke="#D99884" stroke-width="3" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="3" fill="#1B2A4A"/>
</svg>""",

    # 15. Límites
    "15": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#8FA3C4" fill-opacity="0.14"/>
  <line x1="16" y1="78" x2="84" y2="78" stroke="#8FA3C4" stroke-width="1.5"/>
  <line x1="22" y1="16" x2="22" y2="84" stroke="#8FA3C4" stroke-width="1.5"/>
  <path d="M22 68C34 68 42 54 48 44" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <path d="M52 40C58 30 68 24 80 22" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <circle cx="50" cy="42" r="4" fill="#FFFFFF" stroke="#1B2A4A" stroke-width="2.5"/>
  <path d="M38 48L44 45" stroke="#E8B400" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M62 36L56 39" stroke="#D99884" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    # 16. La derivada
    "16": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#FBEAE5" fill-opacity="0.6"/>
  <path d="M16 78H84M22 16V84" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M22 66C32 40 42 28 54 36C66 44 72 60 84 20" stroke="#1B2A4A" stroke-width="3.2" stroke-linecap="round"/>
  <line x1="44" y1="62" x2="80" y2="24" stroke="#1B2A4A" stroke-width="2.6" stroke-linecap="round"/>
  <line x1="44" y1="62" x2="80" y2="24" stroke="#E8B400" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M56 49H66V39" stroke="#D99884" stroke-width="1.8" stroke-linecap="round"/>
  <circle cx="62" cy="43" r="3.5" fill="#E8B400"/>
  <circle cx="62" cy="43" r="1.5" fill="#1B2A4A"/>
</svg>""",

    # 17. La integral
    "17": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#E4EAF4" fill-opacity="0.6"/>
  <path d="M14 74H86M20 14V80" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round"/>
  <rect x="25" y="46" width="9" height="28" rx="1.5" fill="#D99884"/>
  <rect x="35" y="34" width="9" height="40" rx="1.5" fill="#E8B400"/>
  <rect x="45" y="28" width="9" height="46" rx="1.5" fill="#E8B400"/>
  <rect x="55" y="36" width="9" height="38" rx="1.5" fill="#8FA3C4"/>
  <rect x="65" y="48" width="9" height="26" rx="1.5" fill="#8FA3C4"/>
  <path d="M20 62C28 44 38 24 50 26C62 28 68 56 82 44" stroke="#1B2A4A" stroke-width="3" stroke-linecap="round"/>
  <path d="M83 24C83 20 80 18 78 18C75 18 75 22 75 26V34" stroke="#1B2A4A" stroke-width="1.8" stroke-linecap="round" fill="none"/>
</svg>"""
}


def obtener_icono_tema(codigo_tema: str) -> str:
    """Devuelve el SVG correspondiente al código de tema de la sección de práctica."""
    if str(codigo_tema) in ICONOS_TEMAS_PRACTICA:
        return ICONOS_TEMAS_PRACTICA[str(codigo_tema)]
    try:
        cod = int(codigo_tema)
    except (ValueError, TypeError):
        return ICONOS_PARTES["Parte I: Aritmética"]

    if 1 <= cod <= 5:
        return ICONOS_PARTES["Parte I: Aritmética"]
    elif 6 <= cod <= 14:
        return ICONOS_PARTES["Parte II: Álgebra"]
    elif 15 <= cod <= 18:
        return ICONOS_PARTES["Parte III: Funciones"]
    elif 19 <= cod <= 23:
        return ICONOS_PARTES["Parte IV: Geometría euclidiana"]
    elif 24 <= cod <= 29:
        return ICONOS_PARTES["Parte V: Trigonometría"]
    elif 30 <= cod <= 38:
        return ICONOS_PARTES["Parte VI: Geometría analítica"]
    elif 39 <= cod <= 41:
        return ICONOS_PARTES["Parte VII: Cálculo diferencial"]
    elif 42 <= cod <= 44:
        return ICONOS_PARTES["Parte VIII: Cálculo integral"]
    elif 45 <= cod <= 48:
        return ICONOS_PARTES["Parte IX: Probabilidad y estadística"]
    elif 49 <= cod <= 50:
        return ICONOS_PARTES["Parte X: Razonamiento matemático"]
    else:
        return ICONOS_PARTES["Parte XI: Matemáticas financieras"]
