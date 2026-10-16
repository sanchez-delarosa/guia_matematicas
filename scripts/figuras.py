"""
Conversión de figuras TikZ a SVG.

Cada `tikzpicture` se compila con LaTeX real (usando config/comandos.sty y
config/entornos.sty del proyecto original) y se convierte a SVG con dvisvgm.

- Las figuras se identifican por el hash de su código: si una figura no cambia,
  no se vuelve a compilar.
- Todas las figuras nuevas de un capítulo se compilan en un solo documento
  (una página por figura), lo que es mucho más rápido que compilarlas por
  separado. Si ese documento falla, se compilan una por una para aislar
  la figura problemática.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

PREAMBULO = r"""\documentclass[dvisvgm,tikz,border=4pt]{standalone}
\usepackage{libertinus}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-lcroman]{babel}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usetikzlibrary{calc,arrows.meta,positioning,shapes.geometric}
\usepackage{config/comandos}
\usepackage{config/entornos}
\AtBeginDocument{\shorthandoff{<>}}
\begin{document}
"""


def hash_figura(codigo: str) -> str:
    return hashlib.sha1(codigo.strip().encode("utf-8")).hexdigest()[:12]


class CompiladorFiguras:
    def __init__(self, dir_fuente: Path, dir_salida: Path, dir_tmp: Path):
        self.dir_fuente = dir_fuente
        self.dir_salida = dir_salida
        self.dir_tmp = dir_tmp
        self.dir_salida.mkdir(parents=True, exist_ok=True)
        self.dir_tmp.mkdir(parents=True, exist_ok=True)
        self.errores: list[str] = []

    def nombre_svg(self, codigo: str) -> str:
        return f"fig-{hash_figura(codigo)}.svg"

    def compilar(self, figuras: list[str], etiqueta: str) -> None:
        """Compila las figuras que aún no tengan SVG."""
        pendientes = []
        vistos = set()
        for codigo in figuras:
            nombre = self.nombre_svg(codigo)
            if nombre in vistos or (self.dir_salida / nombre).exists():
                continue
            vistos.add(nombre)
            pendientes.append(codigo)
        if not pendientes:
            return
        print(f"  Compilando {len(pendientes)} figura(s) TikZ de {etiqueta}...")
        if not self._compilar_lote(pendientes, etiqueta):
            print("  El lote falló; compilando figuras individualmente...")
            for i, codigo in enumerate(pendientes, 1):
                if not self._compilar_lote([codigo], f"{etiqueta}-{i}"):
                    self.errores.append(f"{etiqueta}: figura {i} no compiló "
                                        f"(ver {self.dir_tmp / (etiqueta + '-' + str(i))}.log)")

    def _compilar_lote(self, figuras: list[str], etiqueta: str) -> bool:
        tex = self.dir_tmp / f"{etiqueta}.tex"
        cuerpo = "\n\n".join(figuras)
        tex.write_text(PREAMBULO + cuerpo + "\n\\end{document}\n", encoding="utf-8")

        r = subprocess.run(
            ["latex", "-interaction=nonstopmode", "-halt-on-error",
             f"--include-directory={self.dir_fuente}", tex.name],
            cwd=self.dir_tmp, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        dvi = tex.with_suffix(".dvi")
        if r.returncode != 0 or not dvi.exists():
            return False

        patron = f"{etiqueta}-p%p.svg"
        r = subprocess.run(
            ["dvisvgm", "--no-fonts=1", "--bbox=6pt", "--exact-bbox",
             "--optimize", "--page=1-", f"--output={patron}", dvi.name],
            cwd=self.dir_tmp, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        if r.returncode != 0:
            print(r.stderr[-2000:])
            return False

        # dvisvgm rellena %p con ceros cuando hay más de 9 páginas;
        # se buscan los archivos generados y se ordenan por número de página.
        generados = sorted(
            self.dir_tmp.glob(f"{etiqueta}-p*.svg"),
            key=lambda p: int(p.stem.rsplit("-p", 1)[1]),
        )
        if len(generados) != len(figuras):
            print(f"  Aviso: se esperaban {len(figuras)} SVG y hay {len(generados)}")
            return False
        for codigo, svg in zip(figuras, generados):
            shutil.move(str(svg), self.dir_salida / self.nombre_svg(codigo))
        return True
