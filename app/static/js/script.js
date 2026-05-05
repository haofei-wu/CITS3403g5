// Timer
const mode_btns = document.querySelectorAll('.mode-btn:not(#custom-btn)');
const custom_btn = document.getElementById('custom-btn');
const timerDisplay = document.getElementById('simple-timer');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');

let timer= null;
let is_running = false;
let modetime = 900
let time_left = 900; // 15 minutes in seconds

// Format time in MM:SS
function formatTime(sec){
    const minutes = Math.floor(sec / 60);
    const seconds = sec % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`; 
}

// update timer display
function timeupdate(){
    timerDisplay.textContent = formatTime(time_left);
}

timeupdate();

// timer mode change
mode_btns.forEach(btn => {

    btn.addEventListener('click', () => {
        const time = parseInt(btn.dataset.time);

        modetime = time;
        time_left = modetime;

        clearActiveState();
        btn.classList.add('active');

        clearInterval(timer);
        is_running = false;
        timer = null;

        startBtn.textContent = 'Start';
        
        timeupdate();
    });
});

// clear active state
function clearActiveState() {
    mode_btns.forEach(btn => btn.classList.remove('active'));
    custom_btn.classList.remove('active');  
}

// custom timer
const customInput = document.getElementById('custom-input');
const customSetBtn = document.getElementById('custom-set');
const customModal = document.getElementById('custom-modal');

custom_btn.addEventListener('click', () => {

    clearActiveState();

    custom_btn.classList.add('active');
    customModal.classList.remove('hidden');

    clearInterval(timer);
    is_running = false;
    timer = null;
    startBtn.textContent = 'Start';
});

customSetBtn.addEventListener('click', () => {
    const minutes = parseInt(customInput.value);
    if (!isNaN(minutes) && minutes > 0) {
        modetime = minutes * 60;
        time_left = modetime;
        customModal.classList.add('hidden');
    }
    timeupdate();  
});

//close window
customModal.addEventListener('click', (e) => {
    if (e.target === customModal) {
        customModal.classList.add('hidden');
    }
});

// start/pause timer
startBtn.addEventListener('click', () => {
    if (!is_running) {
        is_running = true;
        startBtn.textContent = 'Pause';

        timer = setInterval(() => {
            if (time_left > 0) {
                time_left--;
                timeupdate();
            } else {
                clearInterval(timer);
                is_running = false;
                startBtn.textContent = 'Start';
            }
        },1000);

    } else {
        //pause timer
        clearInterval(timer);
        timer = null;
        is_running = false;
        startBtn.textContent = 'Resume';
    }
});


// reset timer
document.getElementById('reset-btn').addEventListener('click', () => {
    clearInterval(timer);
    timer = null;
    is_running = false;
    time_left = modetime; // reset to 15 minutes
    document.getElementById('start-btn').textContent = 'Start';

    timeupdate();
});

let mode = 'add';

// Modechange
function updateModeUI() {
    document.body.classList.toggle('delete-mode', mode === 'delete');

    addBtn.classList.toggle('active', mode === 'add');
    deleteBtn.classList.toggle('active', mode === 'delete');   
}
// Task management
const getcsrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const addBtn = document.getElementById('add-task-btn');
const deleteBtn = document.getElementById('delete-task-btn');

addBtn.addEventListener('click', () => {
    mode = 'add';
    updateModeUI();
})

deleteBtn.addEventListener('click', () => {
    if (mode==='delete') {
        mode = 'add';
    } else {
        mode = 'delete';
    }
    updateModeUI();
});

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
            'Content-Type': 'application/json',
            'X-CSRFToken': getcsrfToken
        },
        body: JSON.stringify({ task: taskInput })
    })
    .then(response => {
        if (response.status === 401) {
            window.location.href = "/login";
            return;
        }
        return response.json()
    })
    .then(data => {
        renderTasks(data.tasks);
        document.getElementById('task-input').value = '';   
    }); 
});

// Render tasks
function renderTasks(tasks) {
    console.log(tasks);
    console.log(tasks[0]);
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        let className = 'task-item';

        if (task.status == true) {
            className = 'task-item completed';
        }

        taskList.innerHTML +=
            `<li class="${className}" id="task-${task.id}">
                <div class="statusbar"></div>
                <span class="statusbox" onclick = "toggleStatus(${task.id})"></span>
                <span>${task.content}</span>
                <button class="delete-btn" onclick="deleteTask(${task.id})">-</button>
            </li>`;
    });
    updateModeUI();
}

// Delete task
function deleteTask(id) {
    if (mode !== 'delete') {
        return;
    }

    fetch(`/delete_tasks/${id}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getcsrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        renderTasks(data.tasks);
    });
}

// status of task
function toggleStatus(id) {
    fetch(`/toggle_status/${id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getcsrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        renderTasks(data.tasks);
    });
}