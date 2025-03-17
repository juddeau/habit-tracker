document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("smoking-form");
    const input = document.getElementById("puffs");
    const progressFill = document.getElementById("progressFill");
    const progressText = document.getElementById("progressText");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let value = parseInt(input.value);
        if (isNaN(value) || value < 0) {
            alert("Введите корректное число сигарет.");
            return;
        }

        // Отправляем данные на сервер
        fetch("/smoking", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "puffs=" + value  // Отправляем данные как "puffs=значение"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text(); // Или response.json(), если сервер возвращает JSON
        })
        .then(data => {
            // Обрабатываем ответ сервера (data)
            console.log("Server response:", data); // Выводим в консоль для отладки

            // Обновляем прогресс
            let progress = Math.max(0, 100 - value * 2); // Пример: чем меньше сигарет, тем выше процент
            progressFill.style.width = progress + "%";
            progressFill.textContent = progress + "%";
            progressText.textContent = progress + "%";

            alert("Данные сохранены! Продолжайте снижать курение.");

            // Очищаем поле ввода
            input.value = "";
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
            alert("Произошла ошибка при сохранении данных.");
        });
    });

    // ... (код для графика остается без изменений) ...
});