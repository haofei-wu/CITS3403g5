const chartdata = window.chartData;
const ctx = document.getElementById('analyticsChart');

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
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

document.getElementById('weekbutton').addEventListener('click', () => {
    window.location.href = '/analyticweek';
});

document.getElementById('daybutton').addEventListener('click', () => {
    window.location.href = '/analyticday';
});

document.getElementById('monthbutton').addEventListener('click', () => {
    window.location.href = '/analyticmonth';
});