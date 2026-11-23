// Fade-in de imágenes + imagen de respaldo si el link falla
document.querySelectorAll('.card img').forEach(img => {
  img.style.opacity = 0;
  img.style.transition = 'opacity .4s';
  const show = () => (img.style.opacity = 1);
  img.complete ? show() : img.addEventListener('load', show);
  img.addEventListener('error', () => { img.src = '/static/img/placeholder.jpg'; show(); });
});

// Borde vino al pasar el cursor sobre la tarjeta
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseenter', () => card.style.borderColor = '#722F4F');
  card.addEventListener('mouseleave', () => card.style.borderColor = '');
});

// ===== DETALLE: agregar al carrito =====
const btnCarrito = document.getElementById('btn-carrito');
if (btnCarrito) {
  btnCarrito.addEventListener('click', async () => {
    btnCarrito.disabled = true;
    try {
      const r = await fetch('/carrito/agregar', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'id=' + encodeURIComponent(btnCarrito.dataset.id)
      });
      if (!r.ok) throw new Error();
      btnCarrito.textContent = 'Agregado ✓';
      btnCarrito.classList.add('ok');
    } catch {
      btnCarrito.textContent = 'Error, intenta de nuevo';
    }
    setTimeout(() => {
      btnCarrito.textContent = 'Agregar a mi carrito +';
      btnCarrito.classList.remove('ok');
      btnCarrito.disabled = false;
    }, 2000);
  });
}
