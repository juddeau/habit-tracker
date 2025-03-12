document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("smoking-form");
    const cigarettesInput = document.getElementById("cigarettes");
    const ctx = document.getElementById("smokingChart").getContext("2d");

    let chartData = {
        labels: [],
        datasets: [{
            label: 'Количество сигарет',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            tension: 0.3
        }]
    };

    let smokingChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: true, // Теперь график не сжимается
            aspectRatio: 2, // Соотношение ширины к высоте
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 20
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const cigarettes = parseInt(cigarettesInput.value);

        if (!isNaN(cigarettes) && cigarettes >= 0) {
            const today = new Date().toLocaleDateString();
            chartData.labels.push(today);
            chartData.datasets[0].data.push(cigarettes);

            let maxCigarettes = Math.max(...chartData.datasets[0].data);
            smokingChart.options.scales.y.suggestedMax = maxCigarettes + 5;

            smokingChart.update();
            cigarettesInput.value = "";
        }
    });
});