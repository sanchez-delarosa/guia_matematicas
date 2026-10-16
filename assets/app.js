// =====================================================
//  Guía de Matemáticas — comportamiento de las páginas
// =====================================================

// --- Fórmulas con KaTeX ---
function dibujarFormulas() {
  if (typeof renderMathInElement !== 'function') return;
  renderMathInElement(document.querySelector('.contenido') || document.body, {
    delimiters: [
      { left: '\\[', right: '\\]', display: true },
      { left: '\\(', right: '\\)', display: false },
    ],
    macros: window.MACROS_KATEX || {},
    throwOnError: false,
    strict: 'ignore',
  });
}
dibujarFormulas();

// --- Índice lateral como cajón en celulares ---
const boton = document.querySelector('.boton-menu');
const lateral = document.querySelector('.indice-lateral');
const velo = document.querySelector('.velo');

function abrirMenu(abrir) {
  if (!lateral) return;
  lateral.classList.toggle('abierto', abrir);
  velo.hidden = !abrir;
  boton.setAttribute('aria-expanded', String(abrir));
}
boton?.addEventListener('click', () => abrirMenu(!lateral.classList.contains('abierto')));
velo?.addEventListener('click', () => abrirMenu(false));
lateral?.addEventListener('click', (e) => { if (e.target.closest('a')) abrirMenu(false); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') abrirMenu(false); });

// --- Resaltar la sección visible en el índice ---
const enlaces = new Map();
document.querySelectorAll('.indice-lateral a[href^="#"]').forEach((a) => {
  enlaces.set(decodeURIComponent(a.getAttribute('href').slice(1)), a);
});
const titulos = [...document.querySelectorAll('.contenido h2[id], .contenido h3[id]')];
if (titulos.length && 'IntersectionObserver' in window) {
  let activo = null;
  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((en) => {
      if (en.isIntersecting) {
        const a = enlaces.get(en.target.id);
        if (a && a !== activo) {
          activo?.classList.remove('activo');
          a.classList.add('activo');
          activo = a;
        }
      }
    });
  }, { rootMargin: '-10% 0px -80% 0px' });
  titulos.forEach((t) => observador.observe(t));
}

// --- Barra de progreso de lectura ---
const progreso = document.querySelector('.progreso');
if (progreso) {
  const actualizar = () => {
    const h = document.documentElement;
    const total = h.scrollHeight - h.clientHeight;
    progreso.style.width = total > 0 ? `${(h.scrollTop / total) * 100}%` : '0';
  };
  document.addEventListener('scroll', actualizar, { passive: true });
  actualizar();
}
