(function () {
  const root = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const navToggle = document.querySelector('.nav-toggle');
  const navList = document.getElementById('primary-nav');
  const year = document.getElementById('year');

  // Year
  if (year) year.textContent = new Date().getFullYear();

  // Theme
  const savedTheme = localStorage.getItem('nova.theme');
  if (savedTheme === 'dark' || savedTheme === 'light') {
    root.setAttribute('data-theme', savedTheme);
  } else {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  }
  updateThemeIcon();

  themeToggle?.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('nova.theme', next);
    updateThemeIcon();
  });

  function updateThemeIcon() {
    if (!themeToggle) return;
    const isDark = root.getAttribute('data-theme') === 'dark';
    themeToggle.textContent = isDark ? '☀️' : '🌙';
    themeToggle.setAttribute('aria-label', isDark ? 'Toggle light mode' : 'Toggle dark mode');
  }

  // Mobile nav
  navToggle?.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    navList?.classList.toggle('open');
  });
  navList?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
    navList.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  }));

  // Smooth scroll focus fix
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href.length < 2) return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (target.tabIndex < 0) target.tabIndex = -1;
      target.focus({ preventScroll: true });
    });
  });

  // Reveal on scroll
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    }
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
})();

