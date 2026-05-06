window.addEventListener("DOMContentLoaded", function () {

    fetch('/get_tasks')
        .then(res => res.json())
        .then(data => {

            renderTaskSummary(data.tasks);

        });

});

function renderTaskSummary(tasks) {

    const container = document.querySelector(".task-summary");

    container.innerHTML = "";

    tasks.sort((a, b) => a.status - b.status);

    const topTasks = tasks.slice(0, 4);

    topTasks.forEach(task => {

        const item = document.createElement("div");

        item.className = "task-item-summary";

        if (task.status) {
            item.classList.add("done");
        }

        item.innerHTML = `
            <span>${task.content}</span>
        `;

        container.appendChild(item);
    });
}