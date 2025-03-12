document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("smoking-form");
    const input = document.getElementById("puffs");
    const progressFill = document.getElementById("progressFill");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let value = parseInt(input.value);
        if (isNaN(value) || value < 0) {
            alert("Введите корректное число сигарет.");
            return;
        }

        // Обновляем прогресс
        let progress = Math.max(0, 100 - value * 2); // Пример: чем меньше сигарет, тем выше процент
        progressFill.style.width = progress + "%";
        progressFill.textContent = progress + "%";

        alert("Данные сохранены! Продолжайте снижать курение.");
    });

    // График курения
    const ctx = document.getElementById("smokingChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            datasets: [{
                label: "Количество сигарет",
                data: [10, 9, 8, 7, 6, 5, 4], // Пример данных
                borderColor: "#2E8B57",
                backgroundColor: "rgba(46, 139, 87, 0.2)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});