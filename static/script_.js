document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider');
    const prevButton = document.querySelector('.btn-prev');
    const nextButton = document.querySelector('.btn-next');
    let scrollAmount = 0;
    const step = 200; // Adjust this value to change the scroll amount

    prevButton.addEventListener('click', function() {
        if (scrollAmount > 0) {
            scrollAmount -= step;
            slider.style.transform = `translateX(-${scrollAmount}px)`;
            updateButtonState();
        }
    });

    nextButton.addEventListener('click', function() {
        const sliderWidth = slider.scrollWidth - slider.clientWidth;
        if (scrollAmount < sliderWidth) {
            scrollAmount += step;
            slider.style.transform = `translateX(-${scrollAmount}px)`;
            updateButtonState();
        }
    });

    function updateButtonState() {
        const sliderWidth = slider.scrollWidth - slider.clientWidth;
        prevButton.classList.toggle('disabled', scrollAmount === 0);
        nextButton.classList.toggle('disabled', scrollAmount >= sliderWidth);
    }

    // Initial button state
    updateButtonState();
});
