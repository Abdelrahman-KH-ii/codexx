(function () {
  'use strict';

  function initNebula() {
    if (typeof gsap === 'undefined') return;

    gsap.to('.nebula-1', {
      x: 40,
      y: -30,
      scale: 1.15,
      duration: 12,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    });

    gsap.to('.nebula-2', {
      x: -50,
      y: 40,
      scale: 1.1,
      duration: 16,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    });

    gsap.to('.nebula-3', {
      x: 30,
      y: 50,
      scale: 0.9,
      duration: 14,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    });

    gsap.from('.hero-headline .line', {
      y: 40,
      opacity: 0,
      duration: 1,
      stagger: 0.15,
      ease: 'power3.out',
      delay: 0.3,
    });

    gsap.from('.hero-sub, .hero-stats, .code-snippet', {
      y: 20,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: 'power2.out',
      delay: 0.6,
    });

    gsap.from('.glass-panel-inner > *', {
      x: 30,
      opacity: 0,
      duration: 0.7,
      stagger: 0.08,
      ease: 'power2.out',
      delay: 0.4,
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNebula);
  } else {
    initNebula();
  }
})();
