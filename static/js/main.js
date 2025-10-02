document.addEventListener('DOMContentLoaded', () => {
  // Set current year in footer
  const yearEl = document.querySelector('[data-current-year]');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // Add fade-in animation to footer
  const footer = document.querySelector('footer');
  if (footer) {
    footer.style.opacity = '0';
    footer.style.transition = 'opacity 0.5s ease-in';
    
    // Trigger the animation after a short delay
    setTimeout(() => {
      footer.style.opacity = '1';
    }, 100);
  }

  // Simple test to verify icons are loading
  setTimeout(() => {
    const socialIcons = document.querySelectorAll('.social-icon i');
    socialIcons.forEach(icon => {
      if (icon.offsetWidth === 0) {
        // If icon is not visible, add a visual indicator
        icon.parentElement.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
        icon.parentElement.style.border = '2px dashed rgba(255, 255, 255, 0.5)';
      }
    });
  }, 1000);

  // Search functionality for country cards (legacy)
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

  // Navbar search form submission
  const navbarSearchForm = document.querySelector('nav .d-flex form');
  if (navbarSearchForm) {
    navbarSearchForm.addEventListener('submit', function(e) {
      const searchInput = this.querySelector('input[name="q"]');
      if (searchInput && searchInput.value.trim() === '') {
        e.preventDefault();
        searchInput.focus();
        return false;
      }
    });
  }
  
  // Enhanced search functionality
  // Add real-time search suggestions
  const searchInputs = document.querySelectorAll('input[name="q"]');
  searchInputs.forEach(input => {
    let searchTimeout;
    
    input.addEventListener('input', function() {
      const query = this.value.trim();
      
      // Clear previous timeout
      clearTimeout(searchTimeout);
      
      // If query is empty, hide suggestions
      if (query === '') {
        hideSearchSuggestions();
        return;
      }
      
      // Set new timeout for debouncing
      searchTimeout = setTimeout(() => {
        performSearch(query);
      }, 300);
    });
    
    // Hide suggestions when input loses focus
    input.addEventListener('blur', function() {
      setTimeout(hideSearchSuggestions, 150);
    });
  });
  
  function performSearch(query) {
    // In a real implementation, this would make an AJAX call to the server
    // For now, we'll just show a simple suggestion
    if (query.length > 2) {
      showSearchSuggestions(query);
    } else {
      hideSearchSuggestions();
    }
  }
  
  function showSearchSuggestions(query) {
    // This is a placeholder for actual search suggestions
    // In a real implementation, this would show dynamic suggestions
    console.log('Searching for:', query);
  }
  
  function hideSearchSuggestions() {
    // This would hide any search suggestions UI
  }

  // Add animation to treatment cards
  const treatmentCards = document.querySelectorAll('.treatment-card');
  treatmentCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      const icon = card.querySelector('.card-img-top i');
      if (icon) {
        icon.style.transform = 'scale(1.2)';
        icon.style.transition = 'transform 0.3s ease';
      }
    });
  
    card.addEventListener('mouseleave', () => {
      const icon = card.querySelector('.card-img-top i');
      if (icon) {
        icon.style.transform = 'scale(1)';
      }
    });
  });

  // Add animation to treatment category cards
  const treatmentCategoryCards = document.querySelectorAll('.treatment-category-card');
  treatmentCategoryCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-5px)';
      card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
  
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });

  // Add hover effect to treatment items
  const treatmentItems = document.querySelectorAll('.treatment-item');
  treatmentItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
      item.style.paddingLeft = '1.25rem';
      item.style.transition = 'padding-left 0.2s ease';
    });
  
    item.addEventListener('mouseleave', () => {
      item.style.paddingLeft = '1rem';
    });
  });

  // Add animation to tab navigation
  const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
  tabLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Remove active class from all tabs
      tabLinks.forEach(l => l.classList.remove('active'));
      // Add active class to clicked tab
      this.classList.add('active');
    });
  });

  // Navbar dropdown behavior - stay open on hover and close on outside click
  const dropdowns = document.querySelectorAll('.navbar .dropdown');
  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
  
    // Show dropdown on hover
    dropdown.addEventListener('mouseenter', () => {
      const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
      if (bsDropdown) {
        bsDropdown.show();
      } else {
        new bootstrap.Dropdown(toggle).show();
      }
    });
  
    // Hide dropdown when mouse leaves the dropdown area
    dropdown.addEventListener('mouseleave', () => {
      setTimeout(() => {
        // Check if mouse is still outside the dropdown
        if (!dropdown.matches(':hover')) {
          const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
          if (bsDropdown) {
            bsDropdown.hide();
          }
        }
      }, 100); // Small delay to allow for smooth movement between toggle and menu
    });
  
    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
      if (!dropdown.contains(event.target)) {
        const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
        if (bsDropdown) {
          bsDropdown.hide();
        }
      }
    });
  });
});