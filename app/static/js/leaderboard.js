function convertTime(seconds, unit) {

    if (unit === "hours") {

        return (seconds / 3600).toFixed(1)
            + " hrs";
    }

    if (unit === "minutes") {

        return Math.floor(seconds / 60)
            + " min";
    }

    return seconds + " sec";
}


function updateTimes() {

    const unit =
        document.getElementById(
            'unitSelect'
        ).value;

    const timeElements =
        document.querySelectorAll(
            '.study-time'
        );

    timeElements.forEach(element => {

        const seconds = parseInt(
            element.dataset.seconds
        );

        element.innerText = convertTime(
            seconds,
            unit
        );
    });
}


document.getElementById(
    'unitSelect'
).addEventListener(
    'change',
    updateTimes
);


updateTimes();

const filterButtons =
    document.querySelectorAll('.filter-btn');


filterButtons.forEach(button => {

    button.addEventListener('click', () => {

        filterButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        button.classList.add('active');
    });
});
