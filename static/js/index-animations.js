// Animated Background Effect
document.addEventListener('DOMContentLoaded', function() {
  // Only run these animations on the index page
  if (document.querySelector('.animated-background')) {
    // Particle effect for background
    const animationCircles = document.querySelectorAll('.animation-circle');
    
    // Add some random movement to the circles
    animationCircles.forEach(circle => {
      const randomDelay = Math.random() * 5;
      const randomDuration = 15 + Math.random() * 10;
      
      circle.style.animationDelay = `${randomDelay}s`;
      circle.style.animationDuration = `${randomDuration}s`;
    });
    
    // Mouse parallax effect
    document.addEventListener('mousemove', function(e) {
      const mouseX = e.clientX / window.innerWidth;
      const mouseY = e.clientY / window.innerHeight;
      
      animationCircles.forEach((circle, index) => {
        const factor = (index + 1) * 15;
        const x = (mouseX * factor) - (factor / 2);
        const y = (mouseY * factor) - (factor / 2);
        
        circle.style.transform = `translate(${x}px, ${y}px)`;
      });
    });
  }
});
