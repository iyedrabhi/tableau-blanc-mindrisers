document.addEventListener('DOMContentLoaded', function () {
  // HERO CAROUSEL
  const hero = document.querySelector('.hero');
  const dots = document.querySelectorAll('.hero-carousel-dots .dot');

  // Images for carousel (use current background as first item)
  const heroImages = [
    '/static/menu/landing/images/hero1.jpg',
    '/static/menu/landing/images/hero2.jpg',
    '/static/menu/landing/images/hero3.jpg'
  ];

  let current = 0;
  let heroInterval = null;
  const HERO_DELAY = 4500;

  function setHero(index) {
    current = index % heroImages.length;
    // update background image while keeping the dark overlay used in CSS
    hero.style.backgroundImage = `linear-gradient(rgba(3,3,3,0.55), rgba(3,3,3,0.55)), url('${heroImages[current]}')`;
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
  }

  function nextHero() {
    setHero((current + 1) % heroImages.length);
  }

  // Init
  if (hero && dots.length) {
    setHero(0);
    heroInterval = setInterval(nextHero, HERO_DELAY);

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', function () {
        setHero(idx);
        // restart interval
        clearInterval(heroInterval);
        heroInterval = setInterval(nextHero, HERO_DELAY);
      });
    });

    // Pause on hover
    hero.addEventListener('mouseenter', () => clearInterval(heroInterval));
    hero.addEventListener('mouseleave', () => {
      clearInterval(heroInterval);
      heroInterval = setInterval(nextHero, HERO_DELAY);
    });
  }

  // TESTIMONIALS AUTO-SCROLL
  const testiContainer = document.querySelector('.testimonials-scroll');
  let testiInterval = null;
  const TESTI_DELAY = 3200;

  function startTestiAutoScroll() {
    if (!testiContainer) return;
    testiInterval = setInterval(() => {
      // width to scroll is the width of the first child (plus gap)
      const first = testiContainer.querySelector('.testi');
      if (!first) return;
      const gap = 18; // matches CSS gap
      const scrollAmount = first.getBoundingClientRect().width + gap;

      // if at the end, scroll back to start smoothly
      if (testiContainer.scrollLeft + testiContainer.clientWidth >= testiContainer.scrollWidth - 10) {
        testiContainer.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        testiContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      }
    }, TESTI_DELAY);
  }

  function stopTestiAutoScroll() {
    if (testiInterval) clearInterval(testiInterval);
  }

  if (testiContainer) {
    startTestiAutoScroll();
    testiContainer.addEventListener('mouseenter', stopTestiAutoScroll);
    testiContainer.addEventListener('mouseleave', startTestiAutoScroll);
    testiContainer.addEventListener('focusin', stopTestiAutoScroll);
    testiContainer.addEventListener('focusout', startTestiAutoScroll);
  }

  // Accessibility: allow left/right arrow to control hero
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      nextHero();
      clearInterval(heroInterval);
      heroInterval = setInterval(nextHero, HERO_DELAY);
    } else if (e.key === 'ArrowLeft') {
      setHero((current - 1 + heroImages.length) % heroImages.length);
      clearInterval(heroInterval);
      heroInterval = setInterval(nextHero, HERO_DELAY);
    }
  });
});
