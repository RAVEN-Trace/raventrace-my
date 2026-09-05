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

  const expandButton = document.querySelector('[data-expand-investments]');
  const investmentList = document.querySelector('[data-investment-list]');
  if (expandButton && investmentList) {
    const records = [...investmentList.querySelectorAll('details')];
    expandButton.addEventListener('click', () => {
      const shouldOpen = !records.every((record) => record.open);
      records.forEach((record) => { record.open = shouldOpen; });
      expandButton.setAttribute('aria-expanded', String(shouldOpen));
      expandButton.textContent = shouldOpen ? 'Tutup semua rekod' : 'Buka semua rekod';
    });

    records.forEach((record) => {
      record.addEventListener('toggle', () => {
        const allOpen = records.every((item) => item.open);
        const allClosed = records.every((item) => !item.open);
        if (allOpen || allClosed) {
          expandButton.setAttribute('aria-expanded', String(allOpen));
          expandButton.textContent = allOpen ? 'Tutup semua rekod' : 'Buka semua rekod';
        }
      });
    });
  }

  const caseNav = document.querySelector('[data-case-nav]');
  if (caseNav && 'IntersectionObserver' in window) {
    const links = [...caseNav.querySelectorAll('a[href^="#"]')];
    const sections = links
      .map((link) => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => {
        link.classList.toggle('active', link.getAttribute('href') === `#${visible.target.id}`);
      });
    }, { rootMargin: '-18% 0px -70% 0px', threshold: [0, 0.15, 0.35] });
    sections.forEach((section) => observer.observe(section));
  }
})();
