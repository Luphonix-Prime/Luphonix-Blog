function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('.nav-list');

    // Mobile menu toggle
    if (mobileMenuToggle && navList) {
        mobileMenuToggle.addEventListener('click', () => {
            navList.classList.toggle('active');
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
}

// Initialize the mobile menu when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
});