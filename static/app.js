document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;

    // Check for user's preference in local storage
    const savedMode = localStorage.getItem('mode');
    if (savedMode) {
        body.classList.add(savedMode);
    } else {
        // If no preference is stored, use default (light mode)
        body.classList.add('light-mode');
    }

    // Toggle between light and dark modes
    function toggleMode() {
        body.classList.toggle('light-mode');
        body.classList.toggle('dark-mode');

        // Save user's preference to local storage
        const currentMode = body.classList.contains('light-mode') ? 'light-mode' : 'dark-mode';
        localStorage.setItem('mode', currentMode);
    }

    // Add event listener to a button or any other trigger
    const modeSwitchButton = document.getElementById('modeSwitchButton');
    if (modeSwitchButton) {
        modeSwitchButton.addEventListener('click', toggleMode);
    }
});
