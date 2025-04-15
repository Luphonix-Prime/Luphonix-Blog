/**
 * luphonix-Blog Blog - Animations
 * Advanced animations for a modern look and feel
 */

/**
 * Initialize scroll reveal animations
 */
function initScrollReveal() {
    // Select all elements with data-animation attribute
    const animatedElements = document.querySelectorAll('[data-animation]');

    // Create an intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // If the element is in the viewport
            if (entry.isIntersecting) {
                // Add the animated class
                entry.target.classList.add('animated');
                // Stop observing the element
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null, // viewport
        threshold: 0.1, // At least 10% of the element is visible
        rootMargin: '0px 0px -100px 0px' // Trigger slightly before the element is in the viewport
    });

    // Observe each element
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Initialize number counters
 */
function initCounters() {
    // Select all counter elements
    const counters = document.querySelectorAll('.counter');

    // Create an intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // If the element is in the viewport
            if (entry.isIntersecting) {
                // Get the target count
                const target = parseInt(entry.target.getAttribute('data-count'), 10);
                // Animate the counter
                animateNumber(entry.target, 0, target, 2000);
                // Stop observing the element
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5 // At least 50% of the element is visible
    });

    // Observe each counter
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

/**
 * Initialize parallax effects
 */
function initParallax() {
    // Select all parallax items
    const parallaxItems = document.querySelectorAll('.parallax-item');

    // Add scroll event listener
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;

        // Update each parallax item
        parallaxItems.forEach(item => {
            const speed = item.getAttribute('data-parallax-speed') || 0.2;
            const direction = item.getAttribute('data-parallax-direction') || 'up';

            let yPos;
            if (direction === 'up') {
                yPos = -scrollY * speed;
            } else {
                yPos = scrollY * speed;
            }

            // Apply the transform
            item.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Initialize text typing effect
 */
function initTypingEffect() {
    // Select all typing effect elements
    const typingElements = document.querySelectorAll('.typing-effect');

    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        
        let i = 0;
        const typingSpeed = parseInt(element.getAttribute('data-typing-speed'), 10) || 100;
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, typingSpeed);
            }
        }
        
        // Start typing
        setTimeout(() => {
            type();
        }, 500);
    });
}

/**
 * Letter animation effect
 * Animates each letter in a text element
 */
class TextLetterAnimation {
    constructor(el) {
        this.el = el;
        this.originalText = el.textContent;
        this.letters = this.originalText.split('');
        this.init();
    }

    init() {
        // Clear the original text
        this.el.textContent = '';
        
        // Create a span for each letter
        this.letters.forEach(letter => {
            const span = document.createElement('span');
            span.textContent = letter;
            this.el.appendChild(span);
        });
        
        // Create intersection observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animate();
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        observer.observe(this.el);
    }

    animate() {
        // Get all letter spans
        const spans = this.el.querySelectorAll('span');
        
        // Animate each letter with a delay
        spans.forEach((span, index) => {
            setTimeout(() => {
                span.style.opacity = 1;
                span.style.transform = 'translateY(0)';
            }, 50 * index);
        });
    }

    reset() {
        this.el.textContent = this.originalText;
    }
}

/**
 * Initialize letter animations
 */
function initLetterAnimations() {
    // Select all letter animation elements
    const letterElements = document.querySelectorAll('.letter-animation');
    
    // Initialize animation for each element
    letterElements.forEach(element => {
        new TextLetterAnimation(element);
    });
}

/**
 * SVG drawing animation
 */
function initSVGAnimations() {
    // Select all SVG elements with animation
    const svgElements = document.querySelectorAll('.svg-animated');
    
    // Create intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe each SVG
    svgElements.forEach(svg => {
        observer.observe(svg);
    });
}

/**
 * Initialize smooth anchor scrolling
 */
function initSmoothScrolling() {
    // Select all links that point to an ID
    const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the target element
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Smooth scroll to the target
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Update URL hash
                history.pushState(null, null, targetId);
            }
        });
    });
}

/**
 * Animate CSS grid items
 */
function animateGrid(gridSelector) {
    const grid = document.querySelector(gridSelector);
    
    if (!grid) return;
    
    // Add animation class to the grid
    grid.classList.add('grid-animation');
    
    // Add grid-item class to all direct children
    Array.from(grid.children).forEach(item => {
        item.classList.add('grid-item');
    });
    
    // Create intersection observer
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            grid.classList.add('animated');
            observer.unobserve(grid);
        }
    }, {
        threshold: 0.2
    });
    
    observer.observe(grid);
}

/**
 * Animate numbers with a counting effect
 */
function animateNumber(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

/**
 * Initialize image comparison slider
 */
function initImageComparison() {
    const comparisons = document.querySelectorAll('.image-comparison');
    
    comparisons.forEach(comparison => {
        const slider = comparison.querySelector('.slider');
        const after = comparison.querySelector('.after');
        
        if (!slider || !after) return;
        
        let isDown = false;
        
        // Mouse events
        slider.addEventListener('mousedown', () => {
            isDown = true;
        });
        
        window.addEventListener('mouseup', () => {
            isDown = false;
        });
        
        window.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            handleMove(e.clientX);
        });
        
        // Touch events
        slider.addEventListener('touchstart', () => {
            isDown = true;
        });
        
        window.addEventListener('touchend', () => {
            isDown = false;
        });
        
        window.addEventListener('touchmove', (e) => {
            if (!isDown) return;
            handleMove(e.touches[0].clientX);
        });
        
        function handleMove(clientX) {
            const rect = comparison.getBoundingClientRect();
            const position = (clientX - rect.left) / rect.width;
            const percentage = position * 100;
            
            // Limit to 0-100%
            const limitedPercentage = Math.max(0, Math.min(100, percentage));
            
            // Update position
            after.style.width = `${limitedPercentage}%`;
            slider.style.left = `${limitedPercentage}%`;
        }
    });
}