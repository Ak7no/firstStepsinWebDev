document.addEventListener('DOMContentLoaded', function() {
    
    const slides = document.querySelectorAll('.carousel-image');
    const totalSlides = slides.length;
    const prevBtn = document.querySelector('.carousel-control-prev');
    const nextBtn = document.querySelector('.carousel-control-next');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        if (slides[index]) {
            slides[index].classList.add('active');
        }
    }

    function changeSlide(direction) {
        currentSlide += direction;

        if (currentSlide >= totalSlides) {
            currentSlide = 0;
        } else if (currentSlide < 0) {
            currentSlide = totalSlides - 1;
        }

        showSlide(currentSlide);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => changeSlide(-1));
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => changeSlide(1));
    }

    if (totalSlides > 0) {
        setInterval(() => {
            changeSlide(1);
        }, 4000);
    }
});