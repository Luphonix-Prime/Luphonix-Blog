function initThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    const icon = themeToggle.querySelector('i');
    const html = document.documentElement;
    
    // Check saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(icon, savedTheme);
    
    // Toggle theme on click
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(icon, newTheme);
    });
}

function updateThemeIcon(icon, theme) {
    if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', initThemeToggle);