document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('.nav-list');

    if (mobileMenuToggle && navList) {
        mobileMenuToggle.addEventListener('click', function() {
            navList.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.main-nav')) {
                navList.classList.remove('active');
            }
        });
    }
});