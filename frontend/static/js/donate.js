document.addEventListener("DOMContentLoaded", function () {
    const fadeInElements = document.querySelectorAll(".fade-in");
    const scaleInElements = document.querySelectorAll(".scale-in");

    function handleScrollAnimation() {
        let triggerBottom = window.innerHeight * 0.85;

        fadeInElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < triggerBottom) {
                el.style.opacity = 1;
                el.style.transform = "translateY(0)";
            }
        });

        scaleInElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < triggerBottom) {
                el.style.opacity = 1;
                el.style.transform = "scale(1)";
            }
        });
    }

    window.addEventListener("scroll", handleScrollAnimation);
    handleScrollAnimation();
});