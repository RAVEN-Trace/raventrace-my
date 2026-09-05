(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');

  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.textContent = open ? 'Tutup' : 'Menu';
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = 'Menu';
        navToggle.focus();
      }
    });
  }

  document.querySelectorAll('[data-share]').forEach((button) => {
    button.addEventListener('click', async () => {
      const payload = {
        title: button.dataset.shareTitle || document.title,
        text: button.dataset.shareText || 'Semak laporan berasaskan bukti ini.',
        url: window.location.href
      };

      try {
        if (navigator.share) {
          await navigator.share(payload);
        } else {
          await navigator.clipboard.writeText(`${payload.text} ${payload.url}`);
          const original = button.textContent;
          button.textContent = 'Pautan disalin';
          window.setTimeout(() => { button.textContent = original; }, 1800);
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          button.textContent = 'Salin gagal';
        }
      }
    });
  });

  const filters = document.querySelectorAll('[data-filter]');
  const items = document.querySelectorAll('[data-topic]');
  filters.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.classList.contains('active')));
    button.addEventListener('click', () => {
      const selected = button.dataset.filter;
      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      items.forEach((item) => {
        item.hidden = selected !== 'all' && item.dataset.topic !== selected;
      });
    });
  });
})();
