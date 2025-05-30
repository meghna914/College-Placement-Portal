// Flash message handling
document.addEventListener('DOMContentLoaded', function() {
  // Close flash messages when the close button is clicked
  const closeButtons = document.querySelectorAll('.flash-message .close-btn');
  closeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      this.parentElement.style.display = 'none';
    });
  });

  // Auto-hide flash messages after 5 seconds
  setTimeout(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
      message.style.opacity = '0';
      setTimeout(() => {
        message.style.display = 'none';
      }, 500);
    });
  }, 5000);

  // Password confirmation validation
  const passwordFields = document.querySelectorAll('input[type="password"]');
  const confirmPasswordFields = document.querySelectorAll('input[id$="confirm-password"]');

  if (passwordFields.length > 0 && confirmPasswordFields.length > 0) {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        const passwordField = form.querySelector('input[name="password"]');
        const confirmField = form.querySelector('input[id$="confirm-password"]');
        
        if (passwordField && confirmField) {
          if (passwordField.value !== confirmField.value) {
            e.preventDefault();
            alert('Passwords do not match!');
          }
        }
      });
    });
  }
});

// Handle tab navigation
function showTab(tabId) {
  // Hide all tabs
  document.querySelectorAll('section[id$="-tab"]').forEach(tab => {
    tab.style.display = 'none';
  });
  
  // Show the selected tab
  document.getElementById(tabId + '-tab').style.display = 'block';
  
  // Update active state
  document.querySelectorAll('.tabs .tab').forEach((tab, index) => {
    tab.classList.remove('active');
  });
  
  // Find the tab with the matching onclick attribute and make it active
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    if (tab.getAttribute('onclick').includes(tabId)) {
      tab.classList.add('active');
    }
  });
}
