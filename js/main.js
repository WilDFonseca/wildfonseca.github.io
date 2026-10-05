(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.links');

  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
      const open = navigation.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(open));
      const isEnglish = document.documentElement.lang === 'en';
      menuButton.setAttribute('aria-label', open ? (isEnglish ? 'Close menu' : 'Fechar menu') : (isEnglish ? 'Open menu' : 'Abrir menu'));
      menuButton.innerHTML = `<i data-lucide="${open ? 'x' : 'menu'}"></i>`;
      window.lucide?.createIcons();
    });
    navigation.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navigation.classList.remove('open');
        menuButton.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // For future translated subpages, use the matching route when it exists.
  // The anchors already point to the localized homepages, so this is an enhancement.
  const currentLocale = document.documentElement.lang === 'en' ? 'en' : 'pt';
  const localizedPath = window.location.pathname.match(/^\/(pt|en)\/(.*)$/);
  if (localizedPath?.[2]) {
    document.querySelectorAll('[data-language-switch]').forEach((link) => {
      const targetLocale = link.dataset.languageSwitch;
      if (targetLocale === localizedPath[1]) return;
      const candidate = `/${targetLocale}/${localizedPath[2]}`;
      fetch(candidate, { method: 'HEAD', credentials: 'same-origin' })
        .then((response) => {
          if (response.ok) link.href = candidate + window.location.search + window.location.hash;
        })
        .catch(() => {});
    });
  }

  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
  window.lucide?.createIcons();
})();
