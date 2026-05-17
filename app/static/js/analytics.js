//gets the chart data from the server
const chartdata = window.chartData;
//gets the canvas element for the analytics chart
const ctx = document.getElementById('analyticsChart');

//generates colors for the chart based on how many tasks the user has
const colors = chartdata.data.map((_, i) =>
    `hsl(${i * 360 / chartdata.data.length}, 70%, 60%)`
  );

//creates the chart
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

//creates the period buttons for the analytics chart and adds event listeners to them
const periodButtons = {
    week: document.getElementById('weekbutton'),
    day: document.getElementById('daybutton'),
    month: document.getElementById('monthbutton')
}

//gets the current period from the query parameters, default to week
const currentPeriod = new URLSearchParams(window.location.search).get('period') || 'week';

Object.entries(periodButtons).forEach(([period, button]) => {
    //if the button is not found, return
    if (!button) {
        return;
    }

    //toggles the active class on the button if the period matches the current period
    button.classList.toggle('active', period === currentPeriod);

    //adds an event listener to the button to update the period when clicked
    button.addEventListener('click', () => {
        window.location.href = `/analytics?period=${period}`;
    });
});