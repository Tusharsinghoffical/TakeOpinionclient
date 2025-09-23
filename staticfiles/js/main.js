document.addEventListener('DOMContentLoaded', () => {
  // Set current year in footer
  const yearEl = document.querySelector('[data-current-year]');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // Search functionality
  const searchInput = document.querySelector('[data-search-input]');
  const grid = document.querySelector(searchInput?.getAttribute('data-search-target') || '');
  if (searchInput && grid) {
    const cards = [...grid.querySelectorAll('[data-country-card]')];
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase().trim();
      cards.forEach(card => {
        const title = (card.getAttribute('data-title') || '').toLowerCase();
        card.style.display = !q || title.includes(q) ? '' : 'none';
      });
    });
  }

  // Add animation to stat counters
  const statItems = document.querySelectorAll('.stat-item .h4');
  statItems.forEach(item => {
    const target = parseInt(item.textContent);
    if (!isNaN(target)) {
      let count = 0;
      const increment = target / 50;
      const timer = setInterval(() => {
        count += increment;
        if (count >= target) {
          item.textContent = target + '+';
          clearInterval(timer);
        } else {
          item.textContent = Math.ceil(count) + '+';
        }
      }, 30);
    }
  });

  // Add hover effect to cards
  const cards = document.querySelectorAll('.card-hover');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-5px)';
      card.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.15)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
      card.style.boxShadow = '';
    });
  });

  // Add smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add animation to section titles when they come into view
  const sectionTitles = document.querySelectorAll('.section-title');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = 1;
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  sectionTitles.forEach(title => {
    title.style.opacity = 0;
    title.style.transform = 'translateY(20px)';
    title.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(title);
  });
});