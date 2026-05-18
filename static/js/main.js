(function () {
  'use strict';

  function initSidebar() {
    var toggle = document.getElementById('sidebar-toggle');
    var sidebar = document.getElementById('sidebar');
    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  function initFlashMessages() {
    document.querySelectorAll('[data-flash]').forEach(function (el) {
      if (typeof gsap !== 'undefined') {
        gsap.from(el, { y: -10, opacity: 0, duration: 0.4 });
        gsap.to(el, {
          opacity: 0,
          y: -10,
          delay: 4,
          duration: 0.4,
          onComplete: function () { el.remove(); },
        });
      }
    });
  }

  function initAnimateCards() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

    gsap.registerPlugin(ScrollTrigger);

    document.querySelectorAll('[data-animate-card]').forEach(function (card, i) {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          start: 'top 90%',
          toggleActions: 'play none none reverse',
        },
        y: 30,
        opacity: 0,
        duration: 0.6,
        delay: i * 0.05,
        ease: 'power2.out',
      });
    });
  }

  function initDashboardEntrance() {
    if (typeof gsap === 'undefined') return;
    var content = document.querySelector('.app-content');
    if (!content || document.querySelector('.hero-split')) return;

    gsap.from('.sidebar', { x: -20, opacity: 0, duration: 0.5, ease: 'power2.out' });
    gsap.from('.topbar', { y: -10, opacity: 0, duration: 0.4, delay: 0.1 });
    gsap.from('.app-content > *', {
      y: 20,
      opacity: 0,
      duration: 0.5,
      stagger: 0.06,
      delay: 0.2,
      ease: 'power2.out',
    });
  }

  function initNewChat() {
    var btn = document.getElementById('new-chat-btn');
    if (btn) {
      btn.addEventListener('click', function () {
        window.location.href = window.location.pathname;
      });
    }
  }

  function init() {
    initSidebar();
    initFlashMessages();
    initAnimateCards();
    initDashboardEntrance();
    initNewChat();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
