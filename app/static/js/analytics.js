const chartdata = window.chartData;
const ctx = document.getElementById('analyticsChart');

if (ctx && window.Chart)
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartdata.labels,
            datasets: [{
                label: 'Hrs Studied Per Task',
                data: chartdata.data,
                borderWidth: 1
            }]
        },
        options: {
            //autofitting
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
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