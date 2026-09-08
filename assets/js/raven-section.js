(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  const close = () => { if (nav && toggle) { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.textContent = 'Menu'; } };
  toggle?.addEventListener('click', () => {
    const open = nav?.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(Boolean(open)));
    toggle.textContent = open ? 'Tutup' : 'Menu';
  });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(); });
  document.querySelector('[data-section-share]')?.addEventListener('click', async (event) => {
    const button = event.currentTarget;
    const payload = { title: document.title, text: document.querySelector('meta[name="description"]').content, url: document.querySelector('link[rel="canonical"]').href };
    try {
      if (navigator.share) await navigator.share(payload);
      else { await navigator.clipboard.writeText(`${payload.text}\n\n${payload.url}`); button.textContent = 'Pautan disalin'; }
    } catch (error) { if (error.name !== 'AbortError') button.textContent = 'Salin gagal'; }
  });
  document.querySelector('[data-expand-investments]')?.addEventListener('click', (event) => {
    const items = [...document.querySelectorAll('details.investment')];
    const open = !items.every((item) => item.open);
    items.forEach((item) => { item.open = open; });
    event.currentTarget.setAttribute('aria-expanded', String(open));
    event.currentTarget.textContent = open ? 'Tutup semua rekod' : 'Buka semua rekod';
  });
})();
