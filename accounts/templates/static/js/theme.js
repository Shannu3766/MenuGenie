// Theme management
const ThemeManager = {
    init() {
        this.themeToggle = document.getElementById('themeToggle');
        this.html = document.documentElement;
        this.icon = this.themeToggle?.querySelector('i');
        
        // Check system preference
        this.systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Initialize theme
        this.initTheme();
        
        // Add event listeners
        this.addEventListeners();
    },

    initTheme() {
        // Get saved theme or use system preference
        const savedTheme = localStorage.getItem('theme');
        const theme = savedTheme || (this.systemPrefersDark ? 'dark' : 'light');
        
        // Apply theme
        this.setTheme(theme);
    },

    setTheme(theme) {
        this.html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateIcon(theme);
        
        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    },

    toggleTheme() {
        const currentTheme = this.html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    },

    updateIcon(theme) {
        if (this.icon) {
            this.icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    },

    addEventListeners() {
        // Theme toggle click
        this.themeToggle?.addEventListener('click', () => this.toggleTheme());

        // System preference change
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
};

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => ThemeManager.init()); 