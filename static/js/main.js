// Enhanced Flash message handling
document.addEventListener('DOMContentLoaded', function() {
  // Initialize flash message system
  initFlashMessages();

  // Initialize form validation
  initFormValidation();

  // Initialize loading states
  initLoadingStates();

  // Initialize tooltips and animations
  initUIEnhancements();
});

function initFlashMessages() {
  // Close flash messages when the close button is clicked
  const closeButtons = document.querySelectorAll('.flash-message .close-btn');
  closeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      hideFlashMessage(this.parentElement);
    });
  });

  // Auto-hide flash messages after 5 seconds
  setTimeout(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
      hideFlashMessage(message);
    });
  }, 5000);
}

function hideFlashMessage(message) {
  message.style.opacity = '0';
  message.style.transform = 'translateX(100%)';
  setTimeout(() => {
    message.style.display = 'none';
  }, 300);
}

function showFlashMessage(text, type = 'info') {
  const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();

  const message = document.createElement('div');
  message.className = `flash-message ${type}`;
  message.innerHTML = `
    ${text}
    <span class="close-btn">&times;</span>
  `;

  flashContainer.appendChild(message);

  // Add close functionality
  message.querySelector('.close-btn').addEventListener('click', () => {
    hideFlashMessage(message);
  });

  // Auto-hide after 5 seconds
  setTimeout(() => {
    hideFlashMessage(message);
  }, 5000);
}

function createFlashContainer() {
  const container = document.createElement('div');
  container.className = 'flash-messages';
  document.body.appendChild(container);
  return container;
}

function initFormValidation() {
  // Password confirmation validation
  const forms = document.querySelectorAll('form');

  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!validateForm(form)) {
        e.preventDefault();
      }
    });

    // Real-time validation
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
      input.addEventListener('blur', () => validateField(input));
      input.addEventListener('input', () => clearFieldError(input));
    });
  });
}

function validateForm(form) {
  let isValid = true;

  // Password confirmation validation
  const passwordField = form.querySelector('input[name="password"]');
  const confirmField = form.querySelector('input[id$="confirm-password"]');

  if (passwordField && confirmField) {
    if (passwordField.value !== confirmField.value) {
      showFieldError(confirmField, 'Passwords do not match!');
      isValid = false;
    }
  }

  // Required field validation
  const requiredFields = form.querySelectorAll('[required]');
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      showFieldError(field, 'This field is required');
      isValid = false;
    }
  });

  // Email validation
  const emailFields = form.querySelectorAll('input[type="email"]');
  emailFields.forEach(field => {
    if (field.value && !isValidEmail(field.value)) {
      showFieldError(field, 'Please enter a valid email address');
      isValid = false;
    }
  });

  return isValid;
}

function validateField(field) {
  clearFieldError(field);

  if (field.hasAttribute('required') && !field.value.trim()) {
    showFieldError(field, 'This field is required');
    return false;
  }

  if (field.type === 'email' && field.value && !isValidEmail(field.value)) {
    showFieldError(field, 'Please enter a valid email address');
    return false;
  }

  return true;
}

function showFieldError(field, message) {
  clearFieldError(field);

  field.classList.add('error');
  const errorDiv = document.createElement('div');
  errorDiv.className = 'field-error';
  errorDiv.textContent = message;
  field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
  field.classList.remove('error');
  const existingError = field.parentNode.querySelector('.field-error');
  if (existingError) {
    existingError.remove();
  }
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function initLoadingStates() {
  // Add loading states to forms
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        setLoadingState(submitBtn, true);
      }
    });
  });
}

function setLoadingState(element, isLoading) {
  if (isLoading) {
    element.disabled = true;
    element.classList.add('loading');
    element.dataset.originalText = element.textContent;
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
  } else {
    element.disabled = false;
    element.classList.remove('loading');
    element.textContent = element.dataset.originalText || element.textContent;
  }
}

function initUIEnhancements() {
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

  // Add animation on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.card, .job-card, .job-item, .notification-item').forEach(el => {
    observer.observe(el);
  });
}

// Handle tab navigation
function showTab(tabId) {
  // Hide all tabs
  document.querySelectorAll('section[id$="-tab"]').forEach(tab => {
    tab.style.display = 'none';
  });

  // Show the selected tab
  const targetTab = document.getElementById(tabId + '-tab');
  if (targetTab) {
    targetTab.style.display = 'block';
  }

  // Update active state
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    tab.classList.remove('active');
  });

  // Find the tab with the matching onclick attribute and make it active
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    const onclickAttr = tab.getAttribute('onclick');
    if (onclickAttr && onclickAttr.includes(tabId)) {
      tab.classList.add('active');
    }
  });
}

// Utility functions for API calls
async function makeApiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    const data = await response.json();
    return { success: response.ok, data, status: response.status };
  } catch (error) {
    console.error('API call failed:', error);
    return { success: false, error: error.message };
  }
}

// Enhanced error handling
function handleApiError(result, defaultMessage = 'An error occurred') {
  if (!result.success) {
    const message = result.data?.message || result.error || defaultMessage;
    showFlashMessage(message, 'error');
    return false;
  }
  return true;
}

// Debounce function for search inputs
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Global utility functions
window.PlacementPortal = {
  showTab,
  showFlashMessage,
  setLoadingState,
  makeApiCall,
  handleApiError,
  debounce
};
