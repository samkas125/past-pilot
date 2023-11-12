document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loaderContainer = document.querySelector('.loader-container');

    form.addEventListener('submit', function() {
        loaderContainer.style.display = 'block';
    });
});