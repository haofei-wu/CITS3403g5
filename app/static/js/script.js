document.addEventListener('DOMContentLoaded', () => {

    const btn = document.getElementById('menubtn');
    const menu_sidebar = document.getElementById('menusidebar');
    const overlay = document.getElementById('overlay');
    
    btn.addEventListener('click', () => {
        menu_sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    });

    overlay.addEventListener('click', () => {
        menu_sidebar.classList.remove('show');
        overlay.classList.remove('show');
    });
});

// Timer
const mode_btns = document.querySelectorAll('.mode-btn');
const timerDisplay = document.getElementById('simple-timer');

function formatTime(sec){
    const minutes = Math.floor(sec / 60);
    const seconds = sec % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`; 
}

mode_btns.forEach(btn => {
    btn.addEventListener('click', () => {
        mode_btns.forEach(b => b.classList.remove('active'));

        btn.classList.add('active');
        
        const time = parseInt(btn.getAttribute('data-time'));
        timerDisplay.textContent = formatTime(time);
    });
});

// Task management
window.onload = function() {
    fetch('/get_tasks')
    .then(response => response.json())
    .then(data => {
        renderTasks(data.tasks);
    });
}

// Add task
document.getElementById('add-task-btn').addEventListener('click', () => {
    const taskInput = document.getElementById('task-input').value;

    fetch('/add_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  
        },
        body: JSON.stringify({ task: taskInput })
    })
    .then(response => response.json())
    .then(data => {
        renderTasks(data.tasks);
        document.getElementById('task-input').value = '';   
    });
}); 

// Render tasks
function renderTasks(tasks) {
    console.log(tasks);
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        taskList.innerHTML +=
            `<li class="task-item" id ="task-${task.id}">
            <span>${task.content}</span>
            <button class="delete-btn" onclick="deleteTask(${task.id})">-</button>
            </li>`;
    });
}

// Delete task
function deleteTask(id) {
    fetch(`/delete_tasks/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        renderTasks(data.tasks);
    });
}