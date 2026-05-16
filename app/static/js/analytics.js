const chartdata = window.chartData;
const ctx = document.getElementById('analyticsChart');
const colors = chartdata.data.map((_, i) =>
    `hsl(${i * 360 / chartdata.data.length}, 70%, 60%)`
  );

if (ctx && window.Chart)
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartdata.labels,
            datasets: [{
                label: 'Hrs Studied Per Task',
                data: chartdata.data,
                borderWidth: 1,
                backgroundColor: colors
            }]
        },
        options: {
            //autofitting
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hrs Studied Per Task'
                    }
                }
            }
        }
    }
);

const periodButtons = {
    week: document.getElementById('weekbutton'),
    day: document.getElementById('daybutton'),
    month: document.getElementById('monthbutton')
}

const currentPeriod = new URLSearchParams(window.location.search).get('period') || 'week';

Object.entries(periodButtons).forEach(([period, button]) => {
    if (!button) {
        return;
    }

    button.classList.toggle('active', period === currentPeriod);

    button.addEventListener('click', () => {
        window.location.href = `/analytics?period=${period}`;
    });
});