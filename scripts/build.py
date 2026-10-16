"""
Genera el sitio web de la guía a partir de los archivos LaTeX originales.

Uso:
    python scripts/build.py                  # prototipo: solo el capítulo 31
    python scripts/build.py --capitulos 31 7 # capítulos específicos
    python scripts/build.py --todos          # toda la guía

Los archivos originales NO se modifican; solo se leen.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from figuras import CompiladorFiguras          # noqa: E402
from latex2html import Conversor, extraer_soluciones, quitar_comentarios  # noqa: E402
from iconos import obtener_icono_parte, obtener_icono_tema        # noqa: E402

RAIZ_WEB = Path(__file__).resolve().parent.parent
FUENTE = RAIZ_WEB.parent / "guia_matematicas"
SALIDA = RAIZ_WEB / "sitio"
TMP = RAIZ_WEB / ".tmp"
PLANTILLAS = RAIZ_WEB / "plantillas"
ASSETS = RAIZ_WEB / "assets"

TITULO_SITIO = "Guía de Matemáticas"
SUBTITULO_SITIO = "Examen de admisión · UNAM · IPN · CENEVAL"


@dataclass
class InfoCapitulo:
    numero: int
    parte: str
    ruta: str          # p. ej. unidades/06-geometria-analitica/02-la-recta
    titulo: str
    archivo_html: str  # p. ej. 31-la-recta.html


# ----------------------------------------------------------------------
#  Lectura de la estructura del libro
# ----------------------------------------------------------------------

def leer_estructura() -> list[InfoCapitulo]:
    main = (FUENTE / "main.tex").read_text(encoding="utf-8")
    capitulos, parte, n = [], "", 0
    en_main = False
    for linea in main.splitlines():
        if r"\mainmatter" in linea:
            en_main = True
        if r"\backmatter" in linea:
            break
        if not en_main:
            continue
        m = re.match(r"\s*%\s*-+\s*(Parte [^:]+:\s*.+?)\s*-+\s*$", linea)
        if m:
            parte = m.group(1)
            continue
        m = re.match(r"\s*\\include\{(unidades/[^}]+)\}", linea)
        if m:
            n += 1
            ruta = m.group(1)
            tex = (FUENTE / f"{ruta}.tex").read_text(encoding="utf-8")
            t = re.search(r"\\chapter\*?\{(.+?)\}\s*$", quitar_comentarios(tex), re.M)
            titulo = t.group(1) if t else Path(ruta).name
            nombre = Path(ruta).name.split("-", 1)[1]
            capitulos.append(InfoCapitulo(n, parte, ruta, titulo, f"{n:02d}-{nombre}.html"))
    return capitulos


def leer_macros_katex() -> dict[str, str]:
    """Traduce \\newcommand y \\DeclareMathOperator de comandos.sty a macros de KaTeX."""
    tex = quitar_comentarios((FUENTE / "config/comandos.sty").read_text(encoding="utf-8"))
    macros = {}
    for m in re.finditer(r"\\newcommand\{\\(\w+)\}(?:\[(\d)\])?\{(.*)\}\s*$", tex, re.M):
        nombre, cuerpo = m.group(1), m.group(3)
        if "tcb" in cuerpo or "raisebox" in cuerpo or "gdef" in cuerpo or not cuerpo:
            continue
        macros["\\" + nombre] = cuerpo
    for m in re.finditer(r"\\DeclareMathOperator\{\\(\w+)\}\{(\w+)\}", tex):
        macros["\\" + m.group(1)] = rf"\operatorname{{{m.group(2)}}}"
    macros[r"\boxed"] = "#1"
    return macros


# ----------------------------------------------------------------------
#  Plantillas
# ----------------------------------------------------------------------

def plantilla(nombre: str, **valores) -> str:
    texto = (PLANTILLAS / nombre).read_text(encoding="utf-8")
    for clave, valor in valores.items():
        texto = texto.replace("{{" + clave + "}}", str(valor))
    return texto


def html_indice_lateral(res) -> str:
    items = []
    for s in res.secciones:
        clase = "nivel-2" if s.nivel == 2 else "nivel-3"
        num = f'<span class="num">{s.numero}</span> ' if s.numero else ""
        items.append(f'<li class="{clase}"><a href="#{s.ident}">{num}{s.titulo_html}</a></li>')
    return "<ul>" + "".join(items) + "</ul>"


def html_navegacion(cap: InfoCapitulo, construidos: dict[int, InfoCapitulo]) -> str:
    anterior = max((n for n in construidos if n < cap.numero), default=None)
    siguiente = min((n for n in construidos if n > cap.numero), default=None)
    partes = []
    if anterior:
        c = construidos[anterior]
        partes.append(f'<a class="nav-anterior" href="{c.archivo_html}"><span>← Anterior</span>'
                      f'{c.numero}. {html.escape(c.titulo)}</a>')
    else:
        partes.append("<span></span>")
    if siguiente:
        c = construidos[siguiente]
        partes.append(f'<a class="nav-siguiente" href="{c.archivo_html}"><span>Siguiente →</span>'
                      f'{c.numero}. {html.escape(c.titulo)}</a>')
    return '<nav class="nav-capitulos">' + "".join(partes) + "</nav>"


def extraer_subtemas(ruta_tex: Path) -> str:
    """Extrae hasta 3 secciones representativas del archivo LaTeX de la unidad."""
    if not ruta_tex.exists():
        return ""
    try:
        tex = ruta_tex.read_text(encoding="utf-8")
        secs = []
        for m in re.finditer(r"\\section\*?\{([^}]+)\}", tex):
            tit = m.group(1).strip()
            tit = re.sub(r"\\[a-zA-Z]+", "", tit).replace("{", "").replace("}", "").strip()
            if tit and "ejercicio" not in tit.lower() and "resumen" not in tit.lower() and "error" not in tit.lower():
                secs.append(tit)
        return " · ".join(secs[:3])
    except Exception:
        return ""


# ----------------------------------------------------------------------
#  Construcción
# ----------------------------------------------------------------------

def construir(numeros: list[int] | None) -> None:
    t0 = time.time()
    estructura = leer_estructura()
    a_construir = [c for c in estructura if numeros is None or c.numero in numeros]
    if not a_construir:
        sys.exit("No se encontró ningún capítulo con esos números.")

    (SALIDA / "capitulos").mkdir(parents=True, exist_ok=True)
    compilador = CompiladorFiguras(FUENTE, SALIDA / "figuras", TMP)
    macros = leer_macros_katex()
    avisos: dict[str, set[str]] = {}

    def url_figura(codigo: str) -> str:
        return f"../figuras/{compilador.nombre_svg(codigo)}"

    construidos = {c.numero: c for c in a_construir}
    # Conservar en la navegación los capítulos generados en ejecuciones anteriores
    for c in estructura:
        if (SALIDA / "capitulos" / c.archivo_html).exists():
            construidos.setdefault(c.numero, c)

    for cap in a_construir:
        print(f"Capítulo {cap.numero}: {cap.titulo}")
        tex = (FUENTE / f"{cap.ruta}.tex").read_text(encoding="utf-8")

        # Soluciones de los ejercicios propuestos
        soluciones_html = []
        arch_sol = FUENTE / "apendices" / "soluciones" / f"cap{cap.numero:02d}-soluciones.tex"
        if arch_sol.exists():
            conv_sol = Conversor(cap.numero, url_figura)
            soluciones_html = [conv_sol.convertir_fragmento(s)
                               for s in extraer_soluciones(arch_sol.read_text(encoding="utf-8"))]
            compilador.compilar(conv_sol.figuras, f"sol{cap.numero:02d}")
            avisos.setdefault(cap.titulo, set()).update(conv_sol.avisos)

        conv = Conversor(cap.numero, url_figura, soluciones_html)
        res = conv.convertir_capitulo(tex)
        compilador.compilar(res.figuras, f"cap{cap.numero:02d}")
        avisos.setdefault(cap.titulo, set()).update(conv.avisos)
        if conv.cont["ejercicio"] != len(soluciones_html):
            avisos[cap.titulo].add(
                f"Hay {conv.cont['ejercicio']} ejercicios pero {len(soluciones_html)} soluciones")

        pagina = plantilla(
            "capitulo.html",
            titulo_pagina=html.escape(f"{cap.numero}. {res.titulo} · {TITULO_SITIO}"),
            titulo_sitio=TITULO_SITIO,
            parte=html.escape(cap.parte),
            indice_lateral=html_indice_lateral(res),
            contenido=res.html,
            navegacion=html_navegacion(cap, construidos),
            macros=json.dumps(macros),
        )
        (SALIDA / "capitulos" / cap.archivo_html).write_text(pagina, encoding="utf-8")

    # Página principal
    partes_dict: dict[str, list[InfoCapitulo]] = {}
    for c in estructura:
        partes_dict.setdefault(c.parte, []).append(c)

    bloques = []
    for parte, caps in partes_dict.items():
        if ":" in parte:
            etiqueta, nombre = parte.split(":", 1)
            etiqueta, nombre = etiqueta.strip(), nombre.strip()
        else:
            etiqueta, nombre = "Materia", parte.strip()

        svg_icono = obtener_icono_parte(parte)

        items_html = []
        for c in caps:
            subtemas = extraer_subtemas(FUENTE / f"{c.ruta}.tex")
            subtemas_html = f'<span class="secciones-cap">{html.escape(subtemas)}</span>' if subtemas else ""
            if c.numero in construidos:
                items_html.append(
                    f'<li><a href="capitulos/{c.archivo_html}">'
                    f'<span class="num">{c.numero}</span>'
                    f'<div class="cap-info">'
                    f'  <span class="titulo-cap">{html.escape(c.titulo)}</span>'
                    f'  {subtemas_html}'
                    f'</div>'
                    f'<span class="flecha">→</span></a></li>'
                )
            else:
                items_html.append(
                    f'<li class="pendiente">'
                    f'<span class="num">{c.numero}</span>'
                    f'<div class="cap-info">'
                    f'  <span class="titulo-cap">{html.escape(c.titulo)}</span>'
                    f'  {subtemas_html}'
                    f'</div>'
                    f'<span class="etiqueta-pendiente">Próximamente</span></li>'
                )

        cant_caps = len(caps)
        subtitulo_parte = f"{cant_caps} capítulo{'s' if cant_caps != 1 else ''}"

        bloques.append(
            f'<section class="tarjeta-parte">\n'
            f'  <div class="tarjeta-banner">\n'
            f'    <div class="tarjeta-ilustracion" aria-hidden="true">\n'
            f'      {svg_icono}\n'
            f'    </div>\n'
            f'  </div>\n'
            f'  <div class="tarjeta-cuerpo">\n'
            f'    <span class="tarjeta-etiqueta">{html.escape(etiqueta)}</span>\n'
            f'    <h2 class="tarjeta-titulo">{html.escape(nombre)}</h2>\n'
            f'    <p class="tarjeta-subtitulo">{subtitulo_parte}</p>\n'
            f'  </div>\n'
            f'  <div class="tarjeta-accion">\n'
            f'    <button type="button" class="btn-toggle-tarjeta" aria-expanded="false" data-count="{cant_caps}" onclick="toggleTarjeta(this)">\n'
            f'      <span class="btn-texto">Ver capítulos ({cant_caps})</span>\n'
            f'      <svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>\n'
            f'    </button>\n'
            f'  </div>\n'
            f'  <div class="tarjeta-colapsable">\n'
            f'    <div class="tarjeta-colapsable-interior">\n'
            f'      <ol class="tarjeta-lista">\n'
            f'        {"".join(items_html)}\n'
            f'      </ol>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</section>'
        )
    # ------------------------------------------------------------------
    # Reactivos de práctica interactiva (soporta múltiples capítulos JSON)
    # ------------------------------------------------------------------
    dir_reactivos = ASSETS / "reactivos"
    arch_reactivos = ASSETS / "reactivos.json"
    todos_reactivos = []

    archivos_json = sorted(dir_reactivos.glob("*.json")) if dir_reactivos.exists() else []
    if archivos_json:
        for arch in archivos_json:
            try:
                data = json.loads(arch.read_text(encoding="utf-8"))
                reacs = data.get("reactivos", [])
                todos_reactivos.extend(reacs)
            except Exception as e:
                print(f"  Aviso: Error leyendo reactivos de {arch.name}: {e}")
        raw_reactivos = {"reactivos": todos_reactivos}
        # Guardar archivo consolidado para compatibilidad y portabilidad
        arch_reactivos.write_text(json.dumps(raw_reactivos, ensure_ascii=False, indent=2), encoding="utf-8")
    elif arch_reactivos.exists():
        raw_reactivos = json.loads(arch_reactivos.read_text(encoding="utf-8"))
        todos_reactivos = raw_reactivos.get("reactivos", [])
    else:
        raw_reactivos = {"reactivos": []}
        todos_reactivos = []

    temas_dict = {}
    for r in todos_reactivos:
        t_cod = str(r["tema"]["codigo"])
        t_nom = r["tema"]["nombre"]
        s_cod = str(r["subtema"]["codigo"])
        s_nom = r["subtema"]["nombre"]
        if t_cod not in temas_dict:
            temas_dict[t_cod] = {
                "codigo": t_cod,
                "nombre": t_nom,
                "subtemas": {},
                "total": 0
            }
        temas_dict[t_cod]["total"] += 1
        if s_cod not in temas_dict[t_cod]["subtemas"]:
            temas_dict[t_cod]["subtemas"][s_cod] = {
                "codigo": s_cod,
                "nombre": s_nom,
                "count": 0
            }
        temas_dict[t_cod]["subtemas"][s_cod]["count"] += 1

    total_reactivos = len(todos_reactivos)
    total_temas = len(temas_dict)

    indice = plantilla("indice.html", titulo_sitio=TITULO_SITIO, subtitulo=SUBTITULO_SITIO,
                       partes="\n".join(bloques), total=len(estructura),
                       listos=len(construidos), total_reactivos=total_reactivos)
    (SALIDA / "index.html").write_text(indice, encoding="utf-8")

    # Páginas de práctica interactiva y simulador
    if todos_reactivos:
        def render_tarjeta_tema(t_cod: str, t_data: dict) -> str:
            subtemas_items = []
            for s_cod, s_data in sorted(
                t_data["subtemas"].items(),
                key=lambda x: [int(p) if p.isdigit() else p for p in x[0].split(".")]
            ):
                subtemas_items.append(
                    f'<li class="subtema-item">\n'
                    f'  <div class="subtema-info">\n'
                    f'    <span class="subtema-codigo">{html.escape(s_cod)}</span>\n'
                    f'    <span class="subtema-nombre">{html.escape(s_data["nombre"])}</span>\n'
                    f'  </div>\n'
                    f'  <a href="simulador.html?subtema={s_cod}" class="btn-subtema-practica">\n'
                    f'    Practicar ({s_data["count"]}) →\n'
                    f'  </a>\n'
                    f'</li>'
                )

            cant_sub = len(t_data["subtemas"])
            cant_reactivos = t_data["total"]
            subtitulo_tema = f"{cant_sub} subtema{'s' if cant_sub != 1 else ''} · {cant_reactivos} reactivos"

            return (
                f'<article class="tarjeta-parte tarjeta-practica" data-tema="{t_cod}">\n'
                f'  <div class="tarjeta-cuerpo">\n'
                f'    <span class="tarjeta-etiqueta tarjeta-etiqueta-practica">Tema {t_cod}</span>\n'
                f'    <h3 class="tarjeta-titulo">{html.escape(t_data["nombre"])}</h3>\n'
                f'    <p class="tarjeta-subtitulo">{subtitulo_tema}</p>\n'
                f'  </div>\n'
                f'  <div class="tarjeta-accion">\n'
                f'    <a href="simulador.html?tema={t_cod}" class="btn-iniciar-practica">\n'
                f'      <span>🎯 Practicar tema completo ({cant_reactivos})</span>\n'
                f'    </a>\n'
                f'    <button type="button" class="btn-toggle-tarjeta" aria-expanded="false" data-count="{cant_sub}" onclick="toggleTarjeta(this)">\n'
                f'      <span class="btn-texto">Ver subtemas ({cant_sub})</span>\n'
                f'      <svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>\n'
                f'    </button>\n'
                f'  </div>\n'
                f'  <div class="tarjeta-colapsable">\n'
                f'    <div class="tarjeta-colapsable-interior">\n'
                f'      <ol class="tarjeta-lista">\n'
                f'        {"".join(subtemas_items)}\n'
                f'      </ol>\n'
                f'    </div>\n'
                f'  </div>\n'
                f'</article>'
            )

        secciones_practica_html = []
        temas_asignados = set()

        for parte, caps in partes_dict.items():
            if ":" in parte:
                etiqueta, nombre = parte.split(":", 1)
                etiqueta, nombre = etiqueta.strip(), nombre.strip()
            else:
                etiqueta, nombre = "Sección", parte.strip()

            tarjetas_seccion = []
            reactivos_seccion = 0
            for c in caps:
                t_cod = str(c.numero)
                if t_cod in temas_dict:
                    temas_asignados.add(t_cod)
                    t_data = temas_dict[t_cod]
                    reactivos_seccion += t_data["total"]
                    tarjetas_seccion.append(render_tarjeta_tema(t_cod, t_data))

            if not tarjetas_seccion:
                continue

            cant_temas_sec = len(tarjetas_seccion)
            svg_icono_parte = obtener_icono_parte(parte)
            resumen_sec = f"{cant_temas_sec} tema{'s' if cant_temas_sec != 1 else ''} · {reactivos_seccion} reactivos"

            secciones_practica_html.append(
                f'<section class="seccion-practica" data-seccion="{html.escape(nombre)}">\n'
                f'  <button type="button" class="seccion-practica-cabecera" aria-expanded="false" data-count="{cant_temas_sec}" onclick="toggleSeccionPractica(this)">\n'
                f'    <div class="seccion-practica-info">\n'
                f'      <div class="seccion-practica-icono" aria-hidden="true">\n'
                f'        {svg_icono_parte}\n'
                f'      </div>\n'
                f'      <div class="seccion-practica-textos">\n'
                f'        <span class="seccion-practica-etiqueta">{html.escape(etiqueta)}</span>\n'
                f'        <h2 class="seccion-practica-titulo">{html.escape(nombre)}</h2>\n'
                f'        <p class="seccion-practica-subtitulo">{resumen_sec}</p>\n'
                f'      </div>\n'
                f'    </div>\n'
                f'    <div class="seccion-practica-accion">\n'
                f'      <span class="btn-seccion-pill">\n'
                f'        <span class="btn-texto-seccion">Ver temas ({cant_temas_sec})</span>\n'
                f'        <svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>\n'
                f'      </span>\n'
                f'    </div>\n'
                f'  </button>\n'
                f'  <div class="seccion-practica-colapsable">\n'
                f'    <div class="seccion-practica-colapsable-interior">\n'
                f'      <div class="seccion-practica-grid">\n'
                f'        {"".join(tarjetas_seccion)}\n'
                f'      </div>\n'
                f'    </div>\n'
                f'  </div>\n'
                f'</section>'
            )

        # Por si hubiera temas adicionales no mapeados en partes_dict
        restantes = [
            (t_cod, t_data) for t_cod, t_data in sorted(
                temas_dict.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0]
            ) if t_cod not in temas_asignados
        ]
        if restantes:
            tarjetas_rest = [render_tarjeta_tema(tc, td) for tc, td in restantes]
            reacs_rest = sum(td["total"] for _, td in restantes)
            cant_rest = len(tarjetas_rest)
            secciones_practica_html.append(
                f'<section class="seccion-practica" data-seccion="Otros temas">\n'
                f'  <button type="button" class="seccion-practica-cabecera" aria-expanded="false" data-count="{cant_rest}" onclick="toggleSeccionPractica(this)">\n'
                f'    <div class="seccion-practica-info">\n'
                f'      <div class="seccion-practica-textos">\n'
                f'        <span class="seccion-practica-etiqueta">Complementario</span>\n'
                f'        <h2 class="seccion-practica-titulo">Otros temas</h2>\n'
                f'        <p class="seccion-practica-subtitulo">{cant_rest} temas · {reacs_rest} reactivos</p>\n'
                f'      </div>\n'
                f'    </div>\n'
                f'    <div class="seccion-practica-accion">\n'
                f'      <span class="btn-seccion-pill">\n'
                f'        <span class="btn-texto-seccion">Ver temas ({cant_rest})</span>\n'
                f'        <svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>\n'
                f'      </span>\n'
                f'    </div>\n'
                f'  </button>\n'
                f'  <div class="seccion-practica-colapsable">\n'
                f'    <div class="seccion-practica-colapsable-interior">\n'
                f'      <div class="seccion-practica-grid">\n'
                f'        {"".join(tarjetas_rest)}\n'
                f'      </div>\n'
                f'    </div>\n'
                f'  </div>\n'
                f'</section>'
            )

        practica_html = plantilla(
            "practica.html",
            titulo_sitio=TITULO_SITIO,
            tarjetas_temas="\n".join(secciones_practica_html),
            total_reactivos=total_reactivos,
            total_temas=total_temas,
            macros=json.dumps(macros)
        )
        (SALIDA / "practica.html").write_text(practica_html, encoding="utf-8")

        simulador_html = plantilla(
            "simulador.html",
            titulo_sitio=TITULO_SITIO,
            datos_json=json.dumps(raw_reactivos, ensure_ascii=False),
            macros=json.dumps(macros)
        )
        (SALIDA / "simulador.html").write_text(simulador_html, encoding="utf-8")

    # Recursos estáticos
    shutil.copytree(ASSETS, SALIDA / "assets", dirs_exist_ok=True)

    # Informe
    print(f"\nListo en {time.time() - t0:.1f} s -> {SALIDA / 'index.html'}")
    for err in compilador.errores:
        print("  ERROR figura:", err)
    for titulo, lista in avisos.items():
        for a in sorted(lista):
            print(f"  Aviso [{titulo}]: {a}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--capitulos", type=int, nargs="+", help="números de capítulo a generar")
    ap.add_argument("--todos", action="store_true", help="generar todos los capítulos")
    ap.add_argument("--salida", type=Path, help="carpeta de salida (por defecto: sitio/)")
    args = ap.parse_args()
    if args.salida:
        SALIDA = args.salida.resolve()
    construir(None if args.todos else (args.capitulos or [31]))
