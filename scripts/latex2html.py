"""
Conversor LaTeX -> HTML adaptado a la guía de matemáticas.

No es un conversor general de LaTeX: está pensado para el subconjunto que usa
la guía (entornos de config/entornos.sty, listas, tablas, secciones, marcas
UNAM/IPN/CENEVAL y matemáticas). Las fórmulas se dejan como LaTeX para que
KaTeX las dibuje en el navegador, y las figuras TikZ se sustituyen por SVG.

Si aparece un comando desconocido, se registra en `self.avisos` para poder
agregarlo después sin romper la conversión.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

# ----------------------------------------------------------------------
#  Configuración de los entornos de entornos.sty
# ----------------------------------------------------------------------

CAJAS = {
    "definicion": "Definición",
    "teorema": "Teorema",
    "ejemplo": "Ejemplo",
    "ejercicio": "Ejercicio",
    "solucion": "Solución",
    "nota": "Nota",
    "advertencia": "Advertencia",
}

ENTORNOS_MATE = r"(align\*?|gather\*?|equation\*?|multline\*?|eqnarray\*?)"

# Comandos que se eliminan junto con sus argumentos: nombre -> nº de argumentos
IGNORAR = {
    "small": 0, "large": 0, "Large": 0, "footnotesize": 0, "scriptsize": 0,
    "normalsize": 0, "centering": 0, "noindent": 0, "par": 0, "clearpage": 0,
    "newpage": 0, "medskip": 0, "bigskip": 0, "smallskip": 0,
    "phantomsection": 0, "raggedright": 0, "hline": 0, "toprule": 0,
    "midrule": 0, "bottomrule": 0, "relax": 0, "protect": 0,
    "vspace": 1, "hspace": 1, "shorthandoff": 1, "shorthandon": 1,
    "setnombrecapitulo": 1, "cline": 1, "arraystretch": 0,
    "addcontentsline": 3, "renewcommand": 2, "setlength": 2,
}

INLINE = {
    "textbf": ("<strong>", "</strong>"),
    "textit": ("<em>", "</em>"),
    "emph": ("<em>", "</em>"),
    "underline": ("<u>", "</u>"),
    "texttt": ("<code>", "</code>"),
    "textsc": ('<span class="sc">', "</span>"),
    "text": ("", ""),
    "mbox": ("", ""),
    "textrm": ("", ""),
    "textnormal": ("", ""),
    "boldmath": ("<strong>", "</strong>"),
}

SIMBOLOS = {
    "%": "%", "&": "&amp;", "$": "$", "#": "#", "_": "_", "{": "{", "}": "}",
    ",": "\u2009", ";": "\u2005", ":": "\u2005", " ": " ", "!": "",
    "quad": "\u2003", "qquad": "\u2003\u2003", "ldots": "…", "dots": "…",
    "textendash": "–", "textemdash": "—", "LaTeX": "LaTeX", "TeX": "TeX",
    "S": "§", "textdegree": "°", "copyright": "©", "checkmark": "✓",
}

MARCAS = {
    "marcaUNAM": ["UNAM"],
    "marcaIPN": ["IPN"],
    "marcaCENEVAL": ["CENEVAL"],
    "marcaTodos": ["UNAM", "IPN", "CENEVAL"],
}

BLOQUE = "\x01"   # delimitador de bloques ya convertidos
TOKEN = "\x00"    # delimitador de fórmulas y figuras protegidas


@dataclass
class Seccion:
    nivel: int
    numero: str
    titulo_html: str
    ident: str


@dataclass
class ResultadoCapitulo:
    titulo: str
    titulo_html: str
    html: str
    secciones: list[Seccion] = field(default_factory=list)
    figuras: list[str] = field(default_factory=list)


def slug(texto: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t or "seccion"


def quitar_comentarios(tex: str) -> str:
    salida = []
    for linea in tex.replace("\r\n", "\n").split("\n"):
        if linea.lstrip().startswith("%"):
            continue  # línea de puro comentario: se elimina por completo
        salida.append(re.sub(r"(?<!\\)%.*$", "", linea))
    return "\n".join(salida)


def quitar_boxed(s: str) -> str:
    """Elimina \\boxed{...} dejando únicamente su contenido, respetando llaves anidadas."""
    while True:
        m = re.search(r"\\boxed\s*\{", s)
        if not m:
            break
        ini = m.start()
        j = m.end() - 1  # posición de '{'
        nivel = 1
        k = j + 1
        escapado = False
        while k < len(s):
            c = s[k]
            if escapado:
                escapado = False
                k += 1
                continue
            if c == "\\":
                escapado = True
                k += 1
                continue
            if c == "{":
                nivel += 1
            elif c == "}":
                nivel -= 1
                if nivel == 0:
                    break
            k += 1
        if nivel == 0:
            s = s[:ini] + s[j + 1:k] + s[k + 1:]
        else:
            s = s[:ini] + s[j + 1:]
            break
    return s


# ----------------------------------------------------------------------
#  Utilidades de análisis
# ----------------------------------------------------------------------

def leer_grupo(s: str, i: int, abre="{", cierra="}") -> tuple[str | None, int]:
    """Si en s[i] (saltando espacios) empieza un grupo, devuelve (contenido, fin)."""
    j = i
    while j < len(s) and s[j] in " \t":
        j += 1
    if j >= len(s) or s[j] != abre:
        return None, i
    nivel = 0
    k = j
    while k < len(s):
        c = s[k]
        if c == "\\":
            k += 2
            continue
        if c == abre:
            nivel += 1
        elif c == cierra:
            nivel -= 1
            if nivel == 0:
                return s[j + 1:k], k + 1
        k += 1
    raise ValueError(f"Grupo sin cerrar cerca de: {s[j:j + 60]!r}")


def buscar_fin_entorno(s: str, nombre: str, desde: int) -> tuple[int, int]:
    """Devuelve (inicio de \\end{nombre}, fin) respetando anidamiento."""
    patron = re.compile(r"\\(begin|end)\{" + re.escape(nombre) + r"\}")
    nivel = 1
    for m in patron.finditer(s, desde):
        nivel += 1 if m.group(1) == "begin" else -1
        if nivel == 0:
            return m.start(), m.end()
    raise ValueError(f"Falta \\end{{{nombre}}}")


def dividir_nivel_superior(s: str, separador: str) -> list[str]:
    """Divide s por `separador` solo fuera de llaves y entornos anidados."""
    partes, actual = [], []
    nivel_llaves = 0
    nivel_entornos = 0
    i = 0
    while i < len(s):
        if s.startswith("\\begin{", i):
            nivel_entornos += 1
        elif s.startswith("\\end{", i):
            nivel_entornos -= 1
        if (nivel_llaves == 0 and nivel_entornos == 0 and s.startswith(separador, i)
                and not (separador[-1].isalpha() and i + len(separador) < len(s)
                         and s[i + len(separador)].isalpha())):
            partes.append("".join(actual))
            actual = []
            i += len(separador)
            continue
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            actual.append(s[i:i + 2])
            i += 2
            continue
        if c == "{":
            nivel_llaves += 1
        elif c == "}":
            nivel_llaves -= 1
        actual.append(c)
        i += 1
    partes.append("".join(actual))
    return partes


# ----------------------------------------------------------------------
#  Conversor
# ----------------------------------------------------------------------

class Conversor:
    def __init__(self, num_capitulo: int, url_figura, soluciones: list[str] | None = None):
        self.num = num_capitulo
        self.url_figura = url_figura          # función: código tikz -> URL del SVG
        self.soluciones = soluciones or []    # HTML de cada solución, en orden
        self.tokens: list[str] = []
        self.bloques: list[str] = []
        self.figuras: list[str] = []
        self.secciones: list[Seccion] = []
        self.avisos: set[str] = set()
        self.cont = {"section": 0, "subsection": 0, "subsubsection": 0,
                     "ejercicio": 0, "ejemplo": 0, "figura": 0}
        self.titulo = ""
        self.titulo_html = ""
        self._ids: set[str] = set()

    # ---------------- protección de fórmulas y figuras ----------------

    def _token(self, contenido_html: str) -> str:
        self.tokens.append(contenido_html)
        return f"{TOKEN}{len(self.tokens) - 1}{TOKEN}"

    def proteger(self, tex: str) -> str:
        # 1) Figuras TikZ
        def fig(m):
            codigo = m.group(0)
            self.figuras.append(codigo)
            self.cont["figura"] += 1
            url = self.url_figura(codigo)
            return self._token(
                f'<img class="figura" src="{url}" alt="Figura {self.num}.{self.cont["figura"]}"'
                f' loading="lazy" decoding="async">'
            )
        tex = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", fig, tex, flags=re.S)

        # 2) Entornos matemáticos de varias líneas -> \[\begin{aligned}..\end{aligned}\]
        def mate_entorno(m):
            nombre, cuerpo = m.group(1), m.group(2)
            base = nombre.rstrip("*")
            if base in ("align", "aligned", "eqnarray"):
                interior = r"\begin{aligned}" + cuerpo + r"\end{aligned}"
            elif base in ("gather", "multline"):
                interior = r"\begin{gathered}" + cuerpo + r"\end{gathered}"
            else:
                interior = cuerpo
            interior = re.sub(r"\\(label|nonumber|notag)(\{[^}]*\})?", "", interior)
            return self._display(interior)
        tex = re.sub(r"\\begin\{" + ENTORNOS_MATE + r"\}(.*?)\\end\{\1\}",
                     mate_entorno, tex, flags=re.S)

        # 3) \[ ... \]  y  $$ ... $$
        tex = re.sub(r"\\\[(.*?)\\\]", lambda m: self._display(m.group(1)), tex, flags=re.S)
        tex = re.sub(r"\$\$(.*?)\$\$", lambda m: self._display(m.group(1)), tex, flags=re.S)

        # 4) $ ... $  y  \( ... \)
        tex = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", lambda m: self._inline(m.group(1)), tex, flags=re.S)
        tex = re.sub(r"\\\((.*?)\\\)", lambda m: self._inline(m.group(1)), tex, flags=re.S)
        return tex

    @staticmethod
    def _limpiar_mate(m: str) -> str:
        m = re.sub(r"\\shorthand(on|off)\{[^}]*\}", "", m)
        m = quitar_boxed(m)
        m = re.sub(r"\\,\s*\^", "^", m)
        m = re.sub(r"[ \t]*\n[ \t]*", " ", m.strip())
        return html.escape(m, quote=False)

    def _display(self, m: str) -> str:
        return self._token(f'<span class="mate-bloque">\\[{self._limpiar_mate(m)}\\]</span>')

    def _inline(self, m: str) -> str:
        return self._token(f"\\({self._limpiar_mate(m)}\\)")

    # ---------------- bloques y párrafos ----------------

    def _bloque(self, contenido_html: str) -> str:
        self.bloques.append(contenido_html)
        return f"\n\n{BLOQUE}{len(self.bloques) - 1}{BLOQUE}\n\n"

    def parrafos(self, texto: str) -> str:
        """Convierte texto ya procesado en párrafos HTML."""
        salida = []
        for trozo in re.split(r"\n\s*\n", texto):
            trozo = trozo.strip()
            if not trozo:
                continue
            m = re.fullmatch(BLOQUE + r"(\d+)" + BLOQUE, trozo)
            if m:
                salida.append(self.bloques[int(m.group(1))])
                continue
            trozo = re.sub(r"\s*\n\s*", " ", trozo)
            # Un párrafo que solo contiene una fórmula en bloque no lleva <p>
            m = re.fullmatch(TOKEN + r"(\d+)" + TOKEN + r"([.,;:]?)", trozo)
            if m and self.tokens[int(m.group(1))].startswith('<span class="mate-bloque">'):
                salida.append(f'<div class="mate">{trozo}</div>')
                continue
            if re.fullmatch(TOKEN + r"(\d+)" + TOKEN, trozo) and \
                    self.tokens[int(trozo.strip(TOKEN))].startswith("<img"):
                salida.append(f'<figure class="fig">{trozo}</figure>')
                continue
            salida.append(f"<p>{trozo}</p>")
        return "\n".join(salida)

    def expandir(self, html_txt: str) -> str:
        """Sustituye bloques y tokens por su contenido final."""
        for _ in range(50):
            nuevo = re.sub(BLOQUE + r"(\d+)" + BLOQUE, lambda m: self.bloques[int(m.group(1))], html_txt)
            nuevo = re.sub(TOKEN + r"(\d+)" + TOKEN, lambda m: self.tokens[int(m.group(1))], nuevo)
            if nuevo == html_txt:
                break
            html_txt = nuevo
        return html_txt

    # ---------------- conversión principal ----------------

    def convertir_capitulo(self, tex: str) -> ResultadoCapitulo:
        tex = self.proteger(quitar_boxed(quitar_comentarios(tex)))
        cuerpo = self.parrafos(self.convertir(tex))
        return ResultadoCapitulo(
            titulo=self.titulo,
            titulo_html=self.expandir(self.titulo_html),
            html=self.expandir(cuerpo),
            secciones=[Seccion(s.nivel, s.numero, self.expandir(s.titulo_html), s.ident)
                       for s in self.secciones],
            figuras=self.figuras,
        )

    def convertir_fragmento(self, tex: str) -> str:
        """Convierte un trozo suelto (p. ej. una solución) a HTML final."""
        tex = self.proteger(quitar_boxed(quitar_comentarios(tex)))
        return self.expandir(self.parrafos(self.convertir(tex)))

    def convertir(self, s: str) -> str:
        """Convierte texto en modo texto. Devuelve texto con bloques/tokens."""
        out: list[str] = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c == "\\":
                i = self._comando(s, i, out)
            elif c == "{":
                contenido, fin = leer_grupo(s, i)
                out.append(self._grupo(contenido))
                i = fin
            elif c == "}":
                i += 1
            elif c == "~":
                out.append("\u00a0")
                i += 1
            elif s.startswith("---", i):
                out.append("—"); i += 3
            elif s.startswith("--", i):
                out.append("–"); i += 2
            elif s.startswith("``", i):
                out.append("“"); i += 2
            elif s.startswith("''", i):
                out.append("”"); i += 2
            elif s.startswith("<<", i):
                out.append("«"); i += 2
            elif s.startswith(">>", i):
                out.append("»"); i += 2
            elif c in "<>&":
                out.append(html.escape(c)); i += 1
            else:
                out.append(c); i += 1
        return "".join(out)

    def _grupo(self, contenido: str) -> str:
        m = re.match(r"\s*\\(bfseries|itshape|em|sffamily)\b\s*", contenido)
        if m:
            resto = self.convertir(contenido[m.end():])
            etiqueta = {"bfseries": "strong", "itshape": "em", "em": "em"}.get(m.group(1))
            return f"<{etiqueta}>{resto}</{etiqueta}>" if etiqueta else resto
        return self.convertir(contenido)

    def _comando(self, s: str, i: int, out: list[str]) -> int:
        # \\ (salto de línea), con argumento opcional [2pt]
        if s.startswith("\\\\", i):
            i += 2
            _, i = leer_grupo(s, i, "[", "]")
            out.append("<br>")
            return i

        m = re.match(r"\\([A-Za-z]+\*?|.)", s[i:])
        nombre = m.group(1)
        j = i + m.end()

        if nombre == "begin":
            return self._entorno(s, i, out)

        if nombre in SIMBOLOS:
            out.append(SIMBOLOS[nombre])
            return j

        if nombre.rstrip("*") in ("chapter", "section", "subsection", "subsubsection"):
            _, j = leer_grupo(s, j, "[", "]")
            titulo, j = leer_grupo(s, j)
            out.append(self._titulo(nombre, titulo))
            return j

        if nombre == "label":
            arg, j = leer_grupo(s, j)
            ident = slug(arg)
            out.append(f'<span id="{ident}" class="ancla"></span>')
            return j

        if nombre in MARCAS:
            _, j = leer_grupo(s, j)  # consume un {} opcional
            out.append(self._marcas(MARCAS[nombre]))
            return j

        if nombre in INLINE:
            arg, j = leer_grupo(s, j)
            a, b = INLINE[nombre]
            out.append(a + (self.convertir(arg) if arg is not None else "") + b)
            return j

        if nombre in IGNORAR:
            for _ in range(IGNORAR[nombre]):
                _, j = leer_grupo(s, j, "[", "]")
                _, j = leer_grupo(s, j)
            if nombre in ("renewcommand", "setlength") and j == i + m.end():
                pass
            return j

        if nombre in ("bfseries", "itshape", "sffamily", "em", "rmfamily", "normalfont"):
            return j  # cambios de fuente sueltos: se ignoran

        if nombre == "texorpdfstring":
            a, j = leer_grupo(s, j)
            _, j = leer_grupo(s, j)
            out.append(self.convertir(a))
            return j

        if nombre in ("ref", "eqref", "pageref"):
            arg, j = leer_grupo(s, j)
            out.append(f'<a href="#{slug(arg)}">↗</a>')
            return j

        if nombre == "item":
            # \item fuera de una lista (no debería ocurrir)
            out.append("• ")
            return j

        if nombre in ("'", "`", "^", '"', "~") and j < len(s):
            # acentos al estilo antiguo: \'a, \~n
            import unicodedata
            marca = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303"}[nombre]
            arg, k = leer_grupo(s, j)
            letra = arg if arg is not None else s[j]
            k = k if arg is not None else j + 1
            letra = letra.replace("\\i", "i")
            out.append(unicodedata.normalize("NFC", letra + marca))
            return k

        self.avisos.add(f"Comando desconocido: \\{nombre}")
        out.append(f'<span class="desconocido">\\{html.escape(nombre)}</span>')
        return j

    # ---------------- títulos ----------------

    def _titulo(self, comando: str, titulo_tex: str) -> str:
        estrella = comando.endswith("*")
        base = comando.rstrip("*")
        titulo_html = self.convertir(titulo_tex)
        
        titulo_sin_mates = re.sub(r"\\\((.*?)\\\)", r"\1", titulo_tex)
        titulo_sin_mates = re.sub(r"\$(.*?)\$", r"\1", titulo_sin_mates)
        texto_plano = self.convertir(titulo_sin_mates)
        texto_plano = re.sub(r"<[^>]+>|" + TOKEN + r"\d+" + TOKEN, "", texto_plano).strip()

        if base == "chapter":
            self.titulo = texto_plano
            self.titulo_html = titulo_html
            return self._bloque(
                f'<header class="cap-encabezado"><p class="cap-numero">Capítulo {self.num}</p>'
                f"<h1>{titulo_html}</h1></header>"
            )

        nivel = {"section": 2, "subsection": 3, "subsubsection": 4}[base]
        numero = ""
        if not estrella:
            if base == "section":
                self.cont["section"] += 1
                self.cont["subsection"] = self.cont["subsubsection"] = 0
                numero = f"{self.num}.{self.cont['section']}"
            elif base == "subsection":
                self.cont["subsection"] += 1
                self.cont["subsubsection"] = 0
                numero = f"{self.num}.{self.cont['section']}.{self.cont['subsection']}"
            else:
                self.cont["subsubsection"] += 1
                numero = (f"{self.num}.{self.cont['section']}.{self.cont['subsection']}"
                          f".{self.cont['subsubsection']}")
        ident = slug(texto_plano)
        base_id, k = ident, 2
        while ident in self._ids:
            ident = f"{base_id}-{k}"; k += 1
        self._ids.add(ident)
        if nivel <= 3:
            self.secciones.append(Seccion(nivel, numero, texto_plano, ident))
        num_html = f'<span class="num">{numero}</span> ' if numero else ""
        return self._bloque(
            f'<h{nivel} id="{ident}">{num_html}{titulo_html}'
            f'<a class="enlace-seccion" href="#{ident}" aria-label="Enlace a esta sección">#</a></h{nivel}>'
        )

    def _marcas(self, examenes: list[str]) -> str:
        spans = "".join(f'<span class="marca marca-{e.lower()}">{e}</span>' for e in examenes)
        return f'<span class="marcas">{spans}</span>'

    # ---------------- entornos ----------------

    def _entorno(self, s: str, i: int, out: list[str]) -> int:
        nombre, j = leer_grupo(s, i + len("\\begin"))
        ini_cuerpo = j
        fin_cuerpo, fin = buscar_fin_entorno(s, nombre, j)
        cuerpo = s[ini_cuerpo:fin_cuerpo]

        if nombre in CAJAS:
            opcional, k = leer_grupo(cuerpo, 0, "[", "]")
            if opcional is not None:
                cuerpo = cuerpo[k:]
            out.append(self._caja(nombre, opcional, cuerpo))
        elif nombre in ("itemize", "enumerate", "description"):
            out.append(self._lista(nombre, cuerpo))
        elif nombre == "center":
            out.append(self._bloque(f'<div class="centro">{self.parrafos(self.convertir(cuerpo))}</div>'))
        elif nombre in ("tabular", "tabular*", "array"):
            out.append(self._tabla(cuerpo))
        elif nombre in ("quote", "quotation"):
            out.append(self._bloque(f"<blockquote>{self.parrafos(self.convertir(cuerpo))}</blockquote>"))
        elif nombre in ("minipage", "scope", "figure", "table", "flushleft", "flushright", "small"):
            cuerpo = re.sub(r"^\s*(\[[^\]]*\])?(\{[^}]*\})?", "", cuerpo, count=1) \
                if nombre == "minipage" else re.sub(r"^\s*\[[^\]]*\]", "", cuerpo, count=1)
            out.append(self._bloque(self.parrafos(self.convertir(cuerpo))))
        else:
            self.avisos.add(f"Entorno desconocido: {nombre}")
            out.append(self._bloque(
                f'<div class="desconocido">[{html.escape(nombre)}]</div>'
                + self.parrafos(self.convertir(cuerpo))))
        return fin

    def _caja(self, tipo: str, opcional: str | None, cuerpo: str) -> str:
        etiqueta = CAJAS[tipo]
        ancla = ""
        if tipo in ("ejercicio", "ejemplo"):
            self.cont[tipo] += 1
            numero = f"{self.num}.{self.cont[tipo]}"
            ancla = f' id="{tipo}-{numero.replace(".", "-")}"'
            titulo = f"{etiqueta} {numero}" + (f". {self.convertir(opcional)}" if opcional else "")
        else:
            titulo = self.convertir(opcional) if opcional else etiqueta
            if opcional and tipo not in ("nota", "advertencia"):
                titulo = f'<span class="tipo">{etiqueta}</span> {titulo}'

        solucion_html = ""
        if tipo == "ejemplo":
            partes = dividir_nivel_superior(cuerpo, "\\textbf{Solución.}")
            if len(partes) > 1:
                cuerpo = partes[0]
                resto = "\\textbf{Solución.}".join(partes[1:])
                solucion_html = self._desplegable("Ver solución", self.parrafos(self.convertir(resto)))
        elif tipo == "ejercicio":
            idx = self.cont["ejercicio"] - 1
            if idx < len(self.soluciones):
                solucion_html = self._desplegable("Ver solución", self.soluciones[idx], "solucion-ejercicio")

        contenido = self.parrafos(self.convertir(cuerpo)) + solucion_html
        return self._bloque(
            f'<section class="caja caja-{tipo}"{ancla}>'
            f'<div class="caja-titulo">{titulo}</div>'
            f'<div class="caja-cuerpo">{contenido}</div></section>'
        )

    @staticmethod
    def _desplegable(resumen: str, contenido: str, clase: str = "") -> str:
        return (f'<details class="solucion {clase}"><summary>{resumen}</summary>'
                f'<div class="solucion-cuerpo">{contenido}</div></details>')

    def _lista(self, tipo: str, cuerpo: str) -> str:
        opciones, k = leer_grupo(cuerpo, 0, "[", "]")
        if opciones is not None:
            cuerpo = cuerpo[k:]
        etiqueta = "ol" if tipo == "enumerate" else "ul"
        estilo = ""
        if opciones:
            if r"\alph" in opciones:
                estilo = ' type="a"'
            elif r"\Alph" in opciones:
                estilo = ' type="A"'
            elif r"\roman" in opciones:
                estilo = ' type="i"'
        items = dividir_nivel_superior(cuerpo, "\\item")[1:]
        lis = []
        for it in items:
            marca, k = leer_grupo(it, 0, "[", "]")
            if marca is not None:
                it = it[k:]
            contenido = self.parrafos(self.convertir(it))
            # Un único párrafo en el ítem: se quita el <p> para que quede compacto
            if contenido.count("<p>") == 1 and contenido.startswith("<p>") and contenido.endswith("</p>"):
                contenido = contenido[3:-4]
            if marca is not None:
                lis.append(f'<li class="con-marca"><span class="marca-item">{self.convertir(marca)}</span> {contenido}</li>')
            else:
                lis.append(f"<li>{contenido}</li>")
        return self._bloque(f"<{etiqueta}{estilo}>" + "".join(lis) + f"</{etiqueta}>")

    def _tabla(self, cuerpo: str) -> str:
        _, k = leer_grupo(cuerpo, 0, "[", "]")
        spec, k = leer_grupo(cuerpo, k)
        cuerpo = cuerpo[k:]
        alineaciones = [{"l": "left", "c": "center", "r": "right"}[c]
                        for c in re.sub(r"\{[^}]*\}|@|\||!|>|<", "", spec or "") if c in "lcr"]
        # Filas antes del primer \midrule -> encabezado
        tiene_encabezado = "\\midrule" in cuerpo
        cuerpo = cuerpo.replace("\\toprule", "")
        filas_html = {"thead": [], "tbody": []}
        seccion = "thead" if tiene_encabezado else "tbody"
        for trozo in re.split(r"\\midrule", cuerpo):
            for fila in dividir_nivel_superior(trozo, "\\\\"):
                fila = re.sub(r"\\(bottomrule|hline|cline\{[^}]*\})", "", fila)
                fila = re.sub(r"^\s*\[[^\]]*\]", "", fila)   # \\[2pt]
                if not fila.strip():
                    continue
                celdas = dividir_nivel_superior(fila, "&")
                tds = []
                for idx, celda in enumerate(celdas):
                    al = alineaciones[idx] if idx < len(alineaciones) else "left"
                    contenido = self.convertir(celda).strip()
                    t = "th" if seccion == "thead" else "td"
                    tds.append(f'<{t} style="text-align:{al}">{contenido}</{t}>')
                filas_html[seccion].append("<tr>" + "".join(tds) + "</tr>")
            seccion = "tbody"
        thead = f"<thead>{''.join(filas_html['thead'])}</thead>" if filas_html["thead"] else ""
        return self._bloque(
            f'<div class="tabla-contenedor"><table>{thead}<tbody>{"".join(filas_html["tbody"])}</tbody></table></div>'
        )


# ----------------------------------------------------------------------
#  Soluciones (apendices/soluciones/capNN-soluciones.tex)
# ----------------------------------------------------------------------

def extraer_soluciones(tex: str) -> list[str]:
    """Devuelve el LaTeX de cada \\item del enumerate de soluciones."""
    tex = quitar_comentarios(tex)
    m = re.search(r"\\begin\{enumerate\}(\[[^\]]*\])?(.*)\\end\{enumerate\}", tex, re.S)
    if not m:
        return []
    items = dividir_nivel_superior(m.group(2), "\\item")[1:]
    return [re.sub(r"^\s*\\textbf\{Solución\.?\}\s*", "", it) for it in items]
