document.addEventListener("DOMContentLoaded", function () {
    const fadeInElements = document.querySelectorAll(".fade-in");
    const slideUpElements = document.querySelectorAll(".slide-up");

    function handleScrollAnimation() {
        let triggerBottom = window.innerHeight * 0.85;

        fadeInElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < triggerBottom) {
                el.classList.add("visible");
            }
        });

        slideUpElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < triggerBottom) {
                el.classList.add("visible");
            }
        });
    }

    window.addEventListener("scroll", handleScrollAnimation);
    handleScrollAnimation();
});