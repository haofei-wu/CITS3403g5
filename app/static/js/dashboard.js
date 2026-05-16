// Run when the DOM is fully loaded
window.addEventListener("DOMContentLoaded", function () {
    // Load tasks for today
    fetch(`/get_tasks?taskdate=${getLocal()}`)
        .then(res => res.json())
        .then(data => {
            renderTaskSummary(data.tasks);
        }
    );
    
    // Get total focus time for today
    const sessiondate = getLocal();

    fetch(`/calculate?sessiondate=${sessiondate}`)
        .then(res => res.json())
        .then(data => {
        document.getElementById("total_focus").textContent = formatFocusTime(data.today_total);
        }
    );

    setupAvatarUpload
});

// Render task summary in the dashboard
function renderTaskSummary(tasks) {

    const container = document.querySelector(".task-summary");
    const count = document.querySelector(".task-count");

    container.innerHTML = "";

    // Show count of done tasks 4/7
    if (count) {
        const doneTasks = tasks.filter(task => task.status).length;
        count.textContent = `${doneTasks}/${tasks.length}`;
    }

    // put done tasks at the end of the list
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

// Format focus time in ms to "hh:mm" format
function formatFocusTime(ms) {
    const totalMinutes = Math.floor(ms / 60000);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return `${String(hours).padStart(2, "0")}h ${String(minutes).padStart(2, "0")}min `;
}

// Get current date in "YYYY-MM-DD" format
function getLocal() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}

// Automatically submit avatar upload form when a file is selected
function setupAvatarUpload() {
    const avatarInput = document.getElementById('avatar-input');
    const avatarForm = document.getElementById('avatar-form');

    if (avatarInput && avatarForm) {
        avatarInput.addEventListener('change', function() {
            if (avatarInput.files.length > 0) {
                avatarForm.submit();
            }
        });
    }
}
