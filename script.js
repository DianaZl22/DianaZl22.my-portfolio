const elements = document.querySelectorAll('.reveal');

window.addEventListener('scroll', () => {
    elements.forEach(el => {
        const top = el.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        if (top < windowHeight - 100) {
            el.classList.add('active');
        }
    });
});