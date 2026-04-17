/* ================================================================
   AI Tools for Pros — site.js
   Dark mode toggle + Mobile hamburger nav
   ================================================================ */
(function () {
  'use strict';

  var DARK_KEY = 'aifp-dark';

  /* ----------------------------------------------------------------
     DARK MODE
  ---------------------------------------------------------------- */
  // window.name persists across page navigations in the same browser tab,
  // including across file:// subdirectory boundaries. Used as a cross-directory
  // fallback for Firefox's per-directory localStorage scope on file:// protocol.
  function parseWinPrefs() {
    try { return JSON.parse(window.name) || {}; } catch (e) { return {}; }
  }
  function saveWinPrefs(prefs) {
    try { window.name = JSON.stringify(prefs); } catch (e) {}
  }

  function isDarkMode() {
    // 1. localStorage — works correctly when served from a real origin (production)
    var saved = localStorage.getItem(DARK_KEY);
    if (saved !== null) return saved === '1';
    // 2. window.name fallback — survives file:// subdirectory changes in the same
    //    tab, fixing Firefox's per-directory localStorage scope on local files
    var prefs = parseWinPrefs();
    if (typeof prefs[DARK_KEY] === 'boolean') return prefs[DARK_KEY];
    // 3. Default: light mode (explicit opt-in only)
    return false;
  }

  function applyDarkMode(on) {
    document.body.classList.toggle('dark-mode', on);
    // Persist to localStorage (production — same origin shares one store)
    localStorage.setItem(DARK_KEY, on ? '1' : '0');
    // Also persist to window.name (local dev — survives file:// dir changes)
    var prefs = parseWinPrefs();
    prefs[DARK_KEY] = on;
    saveWinPrefs(prefs);
    updateDarkIcon(on);
  }

  function updateDarkIcon(on) {
    var btn = document.getElementById('dark-toggle');
    if (!btn) return;
    if (on) {
      // Sun icon (click to go light)
      btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/><path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3.22 3.22l1.06 1.06M11.72 11.72l1.06 1.06M3.22 12.78l1.06-1.06M11.72 4.28l1.06-1.06" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
      btn.setAttribute('aria-label', 'Switch to light mode');
      btn.setAttribute('title', 'Light mode');
    } else {
      // Moon icon (click to go dark)
      btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.5 9.5A5.5 5.5 0 016.5 2.5a5.5 5.5 0 000 11 5.5 5.5 0 007-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      btn.setAttribute('aria-label', 'Switch to dark mode');
      btn.setAttribute('title', 'Dark mode');
    }
  }

  // Apply dark mode immediately (before DOMContentLoaded to avoid flash)
  var dark = isDarkMode();
  if (dark) document.body.classList.add('dark-mode');

  /* ----------------------------------------------------------------
     DOM READY
  ---------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    injectDarkToggle();
    injectHamburger();
    initTouchDropdowns();
    updateDarkIcon(document.body.classList.contains('dark-mode'));
    calcReadingTime();
    initFaqToggles();
    initBackToTop();
  });

  // Reset mobile nav when page is restored from the browser's back/forward cache
  // (bfcache restores the full DOM state, which can leave a sub-panel visually open)
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      var mobileNav = document.getElementById('mobile-nav');
      var burger    = document.getElementById('nav-burger');
      if (mobileNav && burger) {
        // Immediately close (no animation needed on bfcache restore)
        mobileNav.classList.remove('open');
        mobileNav.style.display = 'none';
        mobileNav.setAttribute('aria-hidden', 'true');
        burger.setAttribute('aria-expanded', 'false');
        burger.innerHTML = burgerIcon();
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top      = '';
        document.body.style.width    = '';
      }
    }
  });

  /* ----------------------------------------------------------------
     DARK TOGGLE BUTTON
     Injected into the nav, just before Browse Tools button (or burger)
  ---------------------------------------------------------------- */
  function injectDarkToggle() {
    var nav = document.querySelector('nav');
    if (!nav || document.getElementById('dark-toggle')) return;

    var btn = document.createElement('button');
    btn.id = 'dark-toggle';
    btn.type = 'button';
    // Icon will be set by updateDarkIcon
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13.5 9.5A5.5 5.5 0 016.5 2.5a5.5 5.5 0 000 11 5.5 5.5 0 007-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    btn.onclick = function () {
      applyDarkMode(!document.body.classList.contains('dark-mode'));
    };

    // Insert before Browse Tools or at end of nav
    var browseBtn = document.getElementById('nav-browse-btn');
    if (browseBtn) {
      nav.insertBefore(btn, browseBtn);
    } else {
      nav.appendChild(btn);
    }
  }

  /* ----------------------------------------------------------------
     HAMBURGER MENU — Right drawer with inline accordions
     Single panel slides in from the right.
     "AI Tools" and "Professions" sections expand/collapse in-place.
     Each profession row expands to show its tool links inline.
  ---------------------------------------------------------------- */

  var _scrollY = 0; // saved page scroll offset for iOS body-lock restore

  function injectHamburger() {
    var nav = document.querySelector('nav');
    var navDesktop = document.getElementById('nav-desktop');
    if (!nav || !navDesktop || document.getElementById('nav-burger')) return;

    var burger = document.createElement('button');
    burger.id = 'nav-burger';
    burger.type = 'button';
    burger.setAttribute('aria-label', 'Open menu');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-controls', 'mobile-nav');
    burger.innerHTML = burgerIcon();

    var browseBtn = document.getElementById('nav-browse-btn');
    if (browseBtn) {
      nav.insertBefore(burger, browseBtn);
    } else {
      nav.appendChild(burger);
    }

    var drawer = buildDrawerNav(nav, navDesktop);
    document.body.appendChild(drawer);

    // Backdrop click closes
    drawer.addEventListener('click', function (e) {
      if (e.target === drawer) closeMobileNav(burger, drawer);
    });

    burger.addEventListener('click', function () {
      if (drawer.classList.contains('open')) {
        closeMobileNav(burger, drawer);
      } else {
        openMobileNav(burger, drawer);
      }
    });

    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.keyCode === 27) && drawer.classList.contains('open')) {
        closeMobileNav(burger, drawer);
        burger.focus();
      }
    });
  }

  function openMobileNav(burger, drawer) {
    // Step 1: make wrapper visible (CSS has display:none by default)
    drawer.style.display = 'block';
    // Step 2: force a reflow so the browser registers the display change
    // before we add .open — this is what makes the CSS transition fire
    void drawer.offsetWidth;
    // Step 3: add .open to trigger the backdrop fade + panel slide-in
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    burger.setAttribute('aria-expanded', 'true');
    burger.innerHTML = closeIcon();
    _scrollY = window.scrollY || window.pageYOffset;
    document.body.style.position = 'fixed';
    document.body.style.top      = '-' + _scrollY + 'px';
    document.body.style.width    = '100%';
    document.body.style.overflow = 'hidden';
    var first = drawer.querySelector('.mnav-close');
    if (first) setTimeout(function () { first.focus(); }, 50);
  }

  function closeMobileNav(burger, drawer, skipScrollRestore) {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    burger.setAttribute('aria-expanded', 'false');
    burger.innerHTML = burgerIcon();
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.top      = '';
    document.body.style.width    = '';
    if (!skipScrollRestore) window.scrollTo(0, _scrollY);
    // Hide wrapper after the panel slide-out transition completes (280ms)
    setTimeout(function () {
      if (!drawer.classList.contains('open')) {
        drawer.style.display = 'none';
      }
    }, 300);
  }

  function buildDrawerNav(nav, navDesktop) {
    // Outer wrapper: covers full viewport, backdrop left of panel
    var wrapper = document.createElement('div');
    wrapper.id = 'mobile-nav';
    wrapper.setAttribute('aria-hidden', 'true');

    // Inner panel: slides in from right
    var panel = document.createElement('div');
    panel.className = 'mnav-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-label', 'Navigation menu');

    // ── Header ──────────────────────────────────────────────
    var header = document.createElement('div');
    header.className = 'mnav-header';

    var logoLink = nav.querySelector('a[href*="index"]') || nav.querySelector('a:first-child');
    if (logoLink) {
      var logoA = document.createElement('a');
      logoA.className = 'mnav-logo';
      logoA.href = logoLink.href;
      logoA.setAttribute('aria-label', 'AI Tools for Pros home');
      var img = logoLink.querySelector('img');
      var sp  = logoLink.querySelector('span');
      if (img) logoA.appendChild(img.cloneNode(false));
      if (sp)  logoA.appendChild(sp.cloneNode(true));
      logoA.addEventListener('click', function () { closeMobileNav(document.getElementById('nav-burger'), wrapper); });
      header.appendChild(logoA);
    }

    var closeBtn = document.createElement('button');
    closeBtn.className = 'mnav-close';
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', 'Close menu');
    closeBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 3l12 12M15 3L3 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
    closeBtn.addEventListener('click', function () {
      closeMobileNav(document.getElementById('nav-burger'), wrapper);
      document.getElementById('nav-burger').focus();
    });
    header.appendChild(closeBtn);
    panel.appendChild(header);

    // ── Scrollable body ──────────────────────────────────────
    var body = document.createElement('div');
    body.className = 'mnav-body';

    // Helper: plain link row
    function makeLink(href, text, indent) {
      var a = document.createElement('a');
      a.href = href;
      a.className = indent ? 'mnav-sub-link' : 'mnav-row-link';
      a.textContent = text;
      a.addEventListener('click', function () {
        closeMobileNav(document.getElementById('nav-burger'), wrapper);
      });
      return a;
    }

    // Helper: accordion toggle row (returns {row, content})
    function makeAccordion(labelText, level) {
      var ns = 'http://www.w3.org/2000/svg';

      var row = document.createElement('button');
      row.type = 'button';
      row.className = level === 2 ? 'mnav-acc-row mnav-acc-l2' : 'mnav-acc-row';
      row.setAttribute('aria-expanded', 'false');

      var lbl = document.createElement('span');
      lbl.textContent = labelText;
      row.appendChild(lbl);

      var svg = document.createElementNS(ns, 'svg');
      svg.setAttribute('width', '12');
      svg.setAttribute('height', '12');
      svg.setAttribute('viewBox', '0 0 12 12');
      svg.setAttribute('fill', 'none');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('class', 'mnav-chevron'); /* SVG needs setAttribute, not .className */
      var path = document.createElementNS(ns, 'path');
      path.setAttribute('d', 'M2 4l4 4 4-4');
      path.setAttribute('stroke', 'currentColor');
      path.setAttribute('stroke-width', '1.8');
      path.setAttribute('stroke-linecap', 'round');
      path.setAttribute('stroke-linejoin', 'round');
      svg.appendChild(path);
      row.appendChild(svg);

      var content = document.createElement('div');
      content.className = 'mnav-acc-content';
      content.hidden = true;

      row.addEventListener('click', function () {
        var open = row.getAttribute('aria-expanded') === 'true';
        row.setAttribute('aria-expanded', open ? 'false' : 'true');
        content.hidden = open;
        svg.classList.toggle('mnav-chevron-open', !open);
      });

      return { row: row, content: content };
    }

    // Our Process
    var ourProcess = navDesktop.querySelector('a.nav-link[href*="our-process"]');
    if (ourProcess) body.appendChild(makeLink(ourProcess.href, 'Our Process', false));

    // AI Tools accordion
    var aiDropdown = navDesktop.querySelectorAll('.nav-dropdown')[0];
    if (aiDropdown) {
      var aiAcc = makeAccordion('AI Tools', 1);
      body.appendChild(aiAcc.row);
      aiDropdown.querySelectorAll('a.dropdown-item').forEach(function (a) {
        aiAcc.content.appendChild(makeLink(a.href, a.textContent.trim(), true));
      });
      body.appendChild(aiAcc.content);
    }

    // Professions accordion
    var profDropdown = navDesktop.querySelectorAll('.nav-dropdown')[1];
    if (profDropdown) {
      var profAcc = makeAccordion('Professions', 1);
      body.appendChild(profAcc.row);

      profDropdown.querySelectorAll('.submenu-item').forEach(function (item) {
        var triggerEl = item.querySelector('.submenu-trigger');
        var profName  = triggerEl ? triggerEl.firstChild.textContent.trim() : '';
        if (!profName) return;
        var subLinks = Array.from(item.querySelectorAll('.submenu a'));
        if (!subLinks.length) return;

        // Each profession is a collapsed accordion — click to reveal tool links
        var subAcc = makeAccordion(profName, 2);
        profAcc.content.appendChild(subAcc.row);
        subLinks.forEach(function (link) {
          subAcc.content.appendChild(makeLink(link.href, link.textContent.trim(), true));
        });
        profAcc.content.appendChild(subAcc.content);
      });

      body.appendChild(profAcc.content);
    }

    // Newsletter
    var newsletter = navDesktop.querySelector('a.nav-link[href*="newsletter"]');
    if (newsletter) body.appendChild(makeLink(newsletter.href, 'Newsletter', false));

    panel.appendChild(body);

    // ── Footer CTA ───────────────────────────────────────────
    var browseSrc = document.getElementById('nav-browse-btn');
    if (browseSrc) {
      var footerStrip = document.createElement('div');
      footerStrip.className = 'mnav-footer';
      var cta = document.createElement('a');
      cta.href = browseSrc.href;
      cta.className = 'mnav-cta';
      cta.textContent = 'Browse Tools';
      cta.addEventListener('click', function () { closeMobileNav(document.getElementById('nav-burger'), wrapper); });
      footerStrip.appendChild(cta);
      panel.appendChild(footerStrip);
    }

    wrapper.appendChild(panel);
    return wrapper;
  }

  /* ----------------------------------------------------------------
     TOUCH DROPDOWN SUPPORT
     On touch devices, first tap opens the dropdown (hover doesn't work).
     Second tap navigates. Uses a simple class toggle approach.
  ---------------------------------------------------------------- */
  function initTouchDropdowns() {
    if (!('ontouchstart' in window)) return;

    var dropdowns = document.querySelectorAll('.nav-dropdown');
    dropdowns.forEach(function (dd) {
      var menu = dd.querySelector('.dropdown-menu');
      if (!menu) return;

      dd.addEventListener('touchstart', function (e) {
        var isOpen = dd.classList.contains('touch-open');
        // Close all other dropdowns
        dropdowns.forEach(function (other) {
          if (other !== dd) other.classList.remove('touch-open');
        });
        if (!isOpen) {
          e.preventDefault();
          dd.classList.add('touch-open');
        }
      }, { passive: false });
    });

    // Close on outside tap
    document.addEventListener('touchstart', function (e) {
      if (!e.target.closest('.nav-dropdown')) {
        dropdowns.forEach(function (dd) { dd.classList.remove('touch-open'); });
      }
    }, { passive: true });

    // Submenu touch support
    var subItems = document.querySelectorAll('.submenu-item');
    subItems.forEach(function (item) {
      var sub = item.querySelector('.submenu');
      if (!sub) return;
      item.addEventListener('touchstart', function (e) {
        e.stopPropagation();
        var isOpen = item.classList.contains('touch-open');
        subItems.forEach(function (s) { s.classList.remove('touch-open'); });
        if (!isOpen) {
          e.preventDefault();
          item.classList.add('touch-open');
        }
      }, { passive: false });
    });
  }

  /* ----------------------------------------------------------------
     READING TIME
     Counts words in <main> at 250 WPM and injects into #reading-time.
     Expected byline HTML: ...Published Month DD, YYYY<span id="reading-time"></span>
  ---------------------------------------------------------------- */
  function calcReadingTime() {
    var span = document.getElementById('reading-time');
    if (!span) return;
    var main = document.querySelector('main');
    if (!main) return;
    var text = main.innerText || main.textContent || '';
    var words = text.trim().split(/\s+/).filter(function (w) { return w.length > 0; }).length;
    var mins = Math.max(1, Math.round(words / 250));
    span.innerHTML = '&nbsp;&middot;&nbsp;' + mins + ' min read';
  }

  /* ----------------------------------------------------------------
     FAQ TOGGLES
     Activates collapsible FAQ items for pages using .faq-question /
     .faq-answer / .faq-icon pattern (prose-page template pages).
  ---------------------------------------------------------------- */
  function initFaqToggles() {
    var questions = document.querySelectorAll('.faq-question');
    if (!questions.length) return;
    questions.forEach(function (btn) {
      var item   = btn.closest('.faq-item');
      var answer = item && item.querySelector('.faq-answer');
      var icon   = btn.querySelector('.faq-icon');
      if (!answer) return;
      btn.addEventListener('click', function () {
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        answer.style.display = expanded ? 'none' : 'block';
        if (icon) icon.textContent = expanded ? '+' : '\u2212';
      });
    });
  }

  /* ----------------------------------------------------------------
     BACK TO TOP
     Injects a fixed floating button that appears when the user has
     scrolled ≥ 30% of the page. Smooth-scrolls to the top on click.
     Also handles any existing inline .back-to-top links.
  ---------------------------------------------------------------- */
  function initBackToTop() {
    var legacyBtt = document.getElementById('btt'); // hub pages have a pre-built #btt

    if (legacyBtt) {
      // Hub page: the page ships its own #btt button.
      // Add a 30%-scroll listener that OVERWRITES the page's inline 300px handler
      // (site.js registers after DOMContentLoaded, so our handler fires after the
      // inline one and wins for the final opacity / pointer-events values).
      legacyBtt.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      function onScrollBtt() {
        var scrolled = window.scrollY;
        var total    = document.documentElement.scrollHeight - window.innerHeight;
        var show     = total > 0 && (scrolled / total) >= 0.30;
        legacyBtt.style.opacity       = show ? '1' : '0';
        legacyBtt.style.pointerEvents = show ? 'auto' : 'none';
      }
      window.addEventListener('scroll', onScrollBtt, { passive: true });
      onScrollBtt();
      return;
    }

    // --- Content / cross-reference pages: inject floating button ---
    var floatBtn = document.getElementById('btt-float');
    if (!floatBtn) {
      floatBtn = document.createElement('button');
      floatBtn.id   = 'btt-float';
      floatBtn.type = 'button';
      floatBtn.setAttribute('aria-label', 'Back to top');
      floatBtn.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
        '<path d="M8 13V3M8 3L3 8M8 3l5 5" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round"/></svg>';
      document.body.appendChild(floatBtn);
    }

    floatBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // --- Scroll listener: show at 30% ---
    function onScroll() {
      var scrolled = window.scrollY;
      var total    = document.documentElement.scrollHeight - window.innerHeight;
      var show     = total > 0 && (scrolled / total) >= 0.30;
      floatBtn.classList.toggle('btt-visible', show);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load (handles pre-scrolled restores)

    // --- Also wire up any inline .back-to-top links ---
    document.querySelectorAll('.back-to-top').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  /* ----------------------------------------------------------------
     SVG HELPERS
  ---------------------------------------------------------------- */
  function burgerIcon() {
    return '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
  }
  function closeIcon() {
    return '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 4l12 12M16 4L4 16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
  }

})();
