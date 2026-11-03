document.addEventListener('DOMContentLoaded', function() {
    // Get language preference from localStorage or default to 'en'
    const currentLang = localStorage.getItem('preferred_language') || 'en';
    
    const languageButtons = document.querySelectorAll('.language-btn');
    const contents = document.querySelectorAll('[lang]');

    function setLanguage(lang) {
        // Update buttons
        languageButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });

        // Update content visibility
        contents.forEach(content => {
            content.classList.toggle('active', content.getAttribute('lang') === lang);
        });

        // Update HTML lang attribute
        document.documentElement.setAttribute('lang', lang);
        
        // Save preference
        localStorage.setItem('preferred_language', lang);
    }

    // Add click handlers to language buttons
    languageButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const lang = e.target.dataset.lang;
            setLanguage(lang);
        });
    });

    // Set initial language
    setLanguage(currentLang);
});

// Helper function to add language selector to any page
function addLanguageSelector(targetElement) {
    const selector = document.createElement('div');
    selector.className = 'language-selector';
    selector.innerHTML = `
        <button class="language-btn" data-lang="en">English</button>
        <button class="language-btn" data-lang="es">Español</button>
    `;
    targetElement.appendChild(selector);
}