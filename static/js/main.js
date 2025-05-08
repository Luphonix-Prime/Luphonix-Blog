/**
 * luphonix-Blog Blog - Main JavaScript
 * Core functionality for the website
 */

/**
 * Navigation functionality
 */
function initNavigation() {
    
    const header = document.querySelector('.site-header');
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('.nav-list');
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Handle scroll events for sticky header
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    if (mobileMenuToggle && navList) {
        mobileMenuToggle.addEventListener('click', () => {
            // This line toggles the class on the menu itself
            navList.classList.toggle('active');
            // This line toggles the class on the icon (making it change)
            mobileMenuToggle.classList.toggle('active');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !navList.contains(e.target)) {
                navList.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
            }
        });
    }
    
    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            
            // Update icon
            const icon = themeToggle.querySelector('i');
            if (document.body.classList.contains('light-theme')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
            
            // Save preference
            const theme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
            localStorage.setItem('theme', theme);
        });
        
        // Set initial theme based on saved preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-theme');
            const icon = themeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
}

/**
 * Scroll effects
 */
function initScrollEffects() {
    // Elements that will appear on scroll
    const revealElements = document.querySelectorAll('.reveal');
    
    // Elements that will animate in a staggered fashion
    const staggerLists = document.querySelectorAll('.stagger-list');
    
    // Create intersection observers
    const revealObserver = createObserver(checkReveal);
    const staggerObserver = createObserver(checkStagger);
    
    // Observe elements
    revealElements.forEach(element => {
        revealObserver.observe(element);
    });
    
    staggerLists.forEach(list => {
        staggerObserver.observe(list);
    });
    
    // Function to create an intersection observer
    function createObserver(callback) {
        return new IntersectionObserver((entries) => {
            entries.forEach(callback);
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
    }
    
    // Callback for reveal elements
    function checkReveal(entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            revealObserver.unobserve(entry.target);
        }
    }
    
    // Callback for stagger elements
    function checkStagger(entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('animated');
            staggerObserver.unobserve(entry.target);
        }
    }
}

/**
 * Form handling
 */
function initForms() {
    // Contact form
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Simulate form submission
            fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Your message has been sent successfully!', 'success');
                    contactForm.reset();
                } else {
                    showNotification('There was an error sending your message. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('There was an error sending your message. Please try again.', 'error');
            });
        });
    }
    
    // Newsletter form
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Simulate form submission
            fetch('/api/newsletter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Thank you for subscribing to our newsletter!', 'success');
                    form.reset();
                } else {
                    showNotification('There was an error subscribing. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('There was an error subscribing. Please try again.', 'error');
            });
        });
    });
}

/**
 * Show notification
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, error)
 */
function showNotification(message, type = 'success') {
    // Create notification container if it doesn't exist
    let container = document.querySelector('.notification-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notification-container';
        document.body.appendChild(container);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Add notification content
    notification.innerHTML = `
        <div class="notification-content">${message}</div>
        <button class="notification-close" aria-label="Close">&times;</button>
    `;
    
    // Add to container
    container.appendChild(notification);
    
    // Add event listener for close button
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', () => {
        notification.classList.add('closing');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('closing');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
}

/**
 * Text scramble effect
 */
function initTextScramble() {
    class TextScramble {
        constructor(el) {
            this.el = el;
            this.chars = '!<>-_\\/[]{}—=+*^?#________';
            this.update = this.update.bind(this);
        }
        
        setText(newText) {
            const oldText = this.el.innerText;
            const length = Math.max(oldText.length, newText.length);
            const promise = new Promise((resolve) => this.resolve = resolve);
            this.queue = [];
            
            for (let i = 0; i < length; i++) {
                const from = oldText[i] || '';
                const to = newText[i] || '';
                const start = Math.floor(Math.random() * 40);
                const end = start + Math.floor(Math.random() * 40);
                this.queue.push({ from, to, start, end });
            }
            
            cancelAnimationFrame(this.frameRequest);
            this.frame = 0;
            this.update();
            return promise;
        }
        
        update() {
            let output = '';
            let complete = 0;
            
            for (let i = 0, n = this.queue.length; i < n; i++) {
                let { from, to, start, end, char } = this.queue[i];
                
                if (this.frame >= end) {
                    complete++;
                    output += to;
                } else if (this.frame >= start) {
                    if (!char || Math.random() < 0.28) {
                        char = this.randomChar();
                        this.queue[i].char = char;
                    }
                    output += `<span class="scramble-char">${char}</span>`;
                } else {
                    output += from;
                }
            }
            
            this.el.innerHTML = output;
            
            if (complete === this.queue.length) {
                this.resolve();
            } else {
                this.frameRequest = requestAnimationFrame(this.update);
                this.frame++;
            }
        }
        
        randomChar() {
            return this.chars[Math.floor(Math.random() * this.chars.length)];
        }
    }
    
    // Get all elements with data-scramble
    const scrambleElements = document.querySelectorAll('[data-scramble]');
    
    scrambleElements.forEach(el => {
        const scrambler = new TextScramble(el);
        const originalText = el.textContent;
        
        // Create intersection observer
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                scrambler.setText(originalText);
                observer.unobserve(el);
            }
        }, {
            threshold: 0.5
        });
        
        observer.observe(el);
    });
}

/**
 * Lazy loading images
 */
function initLazyLoading() {
    // Check if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    
                    // Replace src with data-src
                    image.src = image.dataset.src;
                    
                    // Remove data-src attribute
                    image.removeAttribute('data-src');
                    
                    // Stop observing the image
                    imageObserver.unobserve(image);
                }
            });
        });
        
        // Observe each lazy image
        lazyImages.forEach(image => {
            imageObserver.observe(image);
        });
    } else {
        // Fallback for browsers without intersection observer
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        // Load all images immediately
        lazyImages.forEach(image => {
            image.src = image.dataset.src;
            image.removeAttribute('data-src');
        });
    }
}

/**
 * Custom cursor effect
 */
function initCustomCursor() {
    // Check if we're on a touch device
    if ('ontouchstart' in window) return;
    
    // Create cursor elements
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    
    const follower = document.createElement('div');
    follower.className = 'custom-cursor-follower';
    
    // Add to DOM
    document.body.appendChild(cursor);
    document.body.appendChild(follower);
    
    // Mouse move event
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
        
        // The follower follows with a delay
        setTimeout(() => {
            follower.style.left = `${e.clientX}px`;
            follower.style.top = `${e.clientY}px`;
        }, 50);
    });
    
    // Add active class on clickable elements
    const clickables = document.querySelectorAll('a, button, input, textarea, [role="button"]');
    clickables.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('active');
            follower.classList.add('active');
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('active');
            follower.classList.remove('active');
        });
    });
}

/**
 * Page transitions
 */
function initPageTransitions() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);
    
    // Get all internal links
    const links = document.querySelectorAll('a[href^="/"]:not([href^="#"]):not([target="_blank"])');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Skip links with modifiers
            if (e.metaKey || e.ctrlKey || e.shiftKey) return;
            
            e.preventDefault();
            const href = this.getAttribute('href');
            
            // Start transition
            overlay.classList.add('transitioning');
            
            // Navigate after transition
            setTimeout(() => {
                window.location.href = href;
            }, 500);
        });
    });
}

/**
 * GSAP Animations
 */
function initGSAPAnimations() {
    // Check if GSAP is loaded
    if (typeof gsap === 'undefined') return;
    
    // Hero section animation
    if (document.querySelector('.hero-section')) {
        gsap.from('.hero-title', {
            duration: 1,
            y: 50,
            opacity: 0,
            ease: 'power3.out'
        });
        
        gsap.from('.hero-subtitle', {
            duration: 1,
            y: 30,
            opacity: 0,
            delay: 0.3,
            ease: 'power3.out'
        });
        
        gsap.from('.hero-section .btn', {
            duration: 1,
            y: 20,
            opacity: 0,
            delay: 0.6,
            ease: 'power3.out'
        });
        
        gsap.from('.hero-image', {
            duration: 1.2,
            scale: 0.8,
            opacity: 0,
            delay: 0.3,
            ease: 'power3.out'
        });
    }
}

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('nav ul');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', 
                menuToggle.getAttribute('aria-expanded') === 'false' ? 'true' : 'false'
            );
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('nav') && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
});

/**
 * Password validation
 */
function initPasswordValidation() {
    const passwordInput = document.getElementById('password1');
    if (!passwordInput) return;
    
    const requirements = {
        length: { regex: /.{8,}/, element: document.getElementById('length') },
        uppercase: { regex: /[A-Z]/, element: document.getElementById('uppercase') },
        lowercase: { regex: /[a-z]/, element: document.getElementById('lowercase') },
        number: { regex: /[0-9]/, element: document.getElementById('number') },
        special: { regex: /[!@#$%^&*]/, element: document.getElementById('special') }
    };
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        
        // Check each requirement
        for (const [key, requirement] of Object.entries(requirements)) {
            if (requirement.element) {
                if (requirement.regex.test(password)) {
                    requirement.element.classList.add('valid');
                } else {
                    requirement.element.classList.remove('valid');
                }
            }
        }
    });
}

// Initialize all functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize existing functions
    if (typeof initNavigation === 'function') initNavigation();
    if (typeof initScrollEffects === 'function') initScrollEffects();
    if (typeof initForms === 'function') initForms();
    
    // Initialize new password validation
    initPasswordValidation();
});