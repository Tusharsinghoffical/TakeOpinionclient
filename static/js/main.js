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
  function animateStats() {
    console.log('animateStats function called');
    const statItems = document.querySelectorAll('.stat-number');
    console.log('Found', statItems.length, 'stat items');
    
    if (statItems.length === 0) {
      console.log('No stat items found, trying again in 500ms');
      setTimeout(animateStats, 500);
      return;
    }
    
    statItems.forEach((item, index) => {
      const target = parseInt(item.getAttribute('data-target'));
      console.log('Stat item', index, 'target:', target);
      
      // Handle special cases
      const textContent = item.textContent.trim();
      if (textContent === '24/7' || textContent === '100%' || textContent === '100%+') {
        // These are static values, no animation needed
        console.log('Special case text, no animation needed for item', index);
        return;
      }
      
      if (!isNaN(target) && target > 0) {
        // Reset the counter
        item.textContent = '0';
        
        // Use a more gradual animation
        let count = 0;
        const duration = 2000; // 2 seconds
        const steps = 100;
        const increment = target / steps;
        const interval = duration / steps;
        
        console.log('Starting animation for item', index, 'to', target);
        const timer = setInterval(() => {
          count += increment;
          if (count >= target) {
            item.textContent = target.toLocaleString() + '+'; // Add commas for large numbers and plus sign
            clearInterval(timer);
            console.log('Finished animating item', index, 'to', target);
          } else {
            item.textContent = Math.ceil(count).toLocaleString() + '+'; // Add commas for large numbers and plus sign
          }
        }, interval);
      } else {
        console.log('Invalid target for item', index, ':', target);
        // If target is 0 or invalid, just set it to 0
        item.textContent = '0';
      }
    });
  }
  
  // Trigger animation after page load
  window.addEventListener('load', function() {
    console.log('Window loaded, triggering stat animation');
    // Use a longer delay to ensure everything is loaded
    setTimeout(animateStats, 1500);
  });
  
  // Also trigger animation when the stats section comes into view
  document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded');
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
      console.log('Stats section found, setting up observer');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            console.log('Stats section is in view, triggering animation');
            animateStats();
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 }); // Lower threshold to trigger sooner
      
      observer.observe(statsSection);
    } else {
      console.log('Stats section not found in DOM');
      // If stats section not found, try to animate anyway after a delay
      setTimeout(animateStats, 2000);
    }
  });
  
  // Fallback: Try to animate stats every 5 seconds if not already animated
  let statsAnimated = false;
  setInterval(() => {
    if (!statsAnimated) {
      console.log('Fallback: Checking if stats need animation');
      const statItems = document.querySelectorAll('.stat-number');
      if (statItems.length > 0) {
        const firstItem = statItems[0];
        // If the first item still shows 0, animate the stats
        if (firstItem.textContent === '0' && firstItem.getAttribute('data-target') !== '0') {
          console.log('Fallback: Triggering stats animation');
          animateStats();
          statsAnimated = true;
        }
      }
    }
  }, 5000);

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

  // Navbar dropdown behavior - improved for Render deployment
  const dropdowns = document.querySelectorAll('.navbar .dropdown');
  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
  
    // Show dropdown on hover (desktop only)
    dropdown.addEventListener('mouseenter', () => {
      // Only apply hover behavior on larger screens
      if (window.innerWidth > 768) {
        const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
        if (bsDropdown) {
          bsDropdown.show();
        } else {
          new bootstrap.Dropdown(toggle).show();
        }
      }
    });
  
    // Hide dropdown when mouse leaves the dropdown area (desktop only)
    dropdown.addEventListener('mouseleave', () => {
      // Only apply hover behavior on larger screens
      if (window.innerWidth > 768) {
        setTimeout(() => {
          // Check if mouse is still outside the dropdown
          if (!dropdown.matches(':hover')) {
            const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
            if (bsDropdown) {
              bsDropdown.hide();
            }
          }
        }, 100); // Small delay to allow for smooth movement between toggle and menu
      }
    });
  
    // Handle click behavior for mobile/touch devices
    toggle.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      
      const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
      if (bsDropdown) {
        if (toggle.getAttribute('aria-expanded') === 'true') {
          bsDropdown.hide();
        } else {
          bsDropdown.show();
        }
      } else {
        new bootstrap.Dropdown(toggle).toggle();
      }
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
  
  // Ensure navbar collapse works properly on mobile
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.querySelector('.navbar-collapse');
  
  if (navbarToggler && navbarCollapse) {
    navbarToggler.addEventListener('click', function() {
      const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
        toggle: false
      });
      
      if (navbarCollapse.classList.contains('show')) {
        bsCollapse.hide();
      } else {
        bsCollapse.show();
      }
    });
  }
});