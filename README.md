# Guía Interactiva de Matemáticas
> **Examen de admisión · UNAM · IPN · CENEVAL**

Plataforma web interactiva diseñada para la preparación de exámenes de admisión universitaria a nivel superior. El proyecto integra el contenido teórico estructurado en LaTeX con un banco integral de reactivos de práctica y un simulador interactivo en tiempo real con renderizado matemático vía [KaTeX](https://katex.org/).

---

## 🚀 Características principales

- **52 capítulos temáticos** organizados en 11 partes curriculares (Aritmética, Álgebra, Geometría euclidiana, Trigonometría, Geometría analítica, Cálculo diferencial, Cálculo integral, Estadística, Probabilidad, Razonamiento espacial y Matemáticas financieras).
- **4,480 reactivos interactivos** clasificados por capítulo, subtema, habilidad cognitiva y nivel de dificultad.
- **Simulador de examen y práctica por tema:** Modos de entrenamiento por tema completo o por subtema específico con retroalimentación inmediata.
- **Renderizado matemático de alta precisión:** Fórmulas matemáticas en LaTeX renderizadas con KaTeX.
- **Arquitectura estática y ligera:** Generado sin dependencias de backend pesado, listo para alojarse en Netlify, GitHub Pages, Vercel o cualquier servidor web estático.

---

## 📁 Estructura del proyecto

```text
guia_web/
├── assets/
│   ├── app.js               # Lógica del cliente, simulador y navegación
│   ├── estilo.css           # Estilos de la plataforma (diseño responsivo)
│   ├── reactivos.json       # Base de datos consolidada con los 4,480 reactivos
│   └── reactivos/           # Archivos modulares JSON por capítulo (capitulo-01 a 52)
├── plantillas/
│   ├── capitulo.html        # Plantilla para vistas de capítulo teórico
│   ├── indice.html          # Portada principal del temario
│   ├── practica.html        # Catálogo interactivo de temas y subtemas
│   └── simulador.html       # Interfaz del simulador interactivo de reactivos
├── scripts/
│   ├── build.py             # Script principal de generación del sitio web
│   ├── check_reactivos.py   # Verificador de integridad y versiones de reactivos
│   ├── latex2html.py        # Conversor de sintaxis LaTeX a HTML
│   ├── figuras.py           # Compilador de figuras TikZ/PGF a SVG
│   └── iconos.py            # Generador de iconos SVG temáticos
├── sitio/                   # Salida compilada lista para producción
│   ├── index.html
│   ├── practica.html
│   ├── simulador.html
│   └── assets/
├── netlify.toml             # Configuración de despliegue para Netlify
└── .gitignore
```

---

## 🛠️ Requisitos e instalación

- **Python 3.10 o superior**
- *(Opcional)* Distribución de TeX/LaTeX (como TeX Live o MiKTeX) si se desea compilar nuevas figuras o contenido teórico directamente desde los archivos `.tex` fuente.

---

## 💻 Uso

### 1. Servir localmente el sitio compilado
Para explorar la plataforma en tu navegador:
```bash
python -m http.server 8000 --directory sitio
```
Abre en tu navegador: [http://localhost:8000](http://localhost:8000)

### 2. Compilar el sitio web
Para regenerar el sitio web y consolidar la base de datos de reactivos:
```bash
# Prototipo / actualización rápida
python scripts/build.py

# Compilación completa de todos los capítulos
python scripts/build.py --todos
```

### 3. Verificar estado de los reactivos
Para inspeccionar la cantidad de reactivos y versión de cada uno de los 52 capítulos:
```bash
python scripts/check_reactivos.py
```

---

## 🌐 Despliegue

El proyecto está configurado para desplegarse de manera directa:
- **Netlify:** La carpeta de publicación es `sitio/` (preconfigurada en `netlify.toml`).
- **GitHub Pages:** Puede publicarse seleccionando la carpeta raíz o la carpeta `sitio/` desde la configuración del repositorio en *Settings > Pages*.
