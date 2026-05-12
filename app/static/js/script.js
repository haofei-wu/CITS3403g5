// Timer
const mode_btns = document.querySelectorAll('.mode-btn:not(#custom-btn)');
// const custom_btn = document.getElementById('custom-btn');
const timerDisplay = document.getElementById('simple-timer');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');

let timer= null;
let is_running = false;
let worklength = document.getElementById('pom-worklength').textContent;
let short_break = document.getElementById('pom-short-break').textContent;
let long_break = document.getElementById('pom-long-break').textContent;
let modetime = worklength * 60;
let time_left = modetime;

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

// clear active state
function clearActiveState() {
    mode_btns.forEach(btn => btn.classList.remove('active'));
    // custom_btn.classList.remove('active');
}

function length_change(length, button) {
    modetime = length * 60;
    time_left = modetime;

    clearActiveState();

    button.classList.add('active');

    clearInterval(timer);
    is_running = false;
    timer = null;

    startBtn.textContent = 'Start';
    
    timeupdate();
}
const workbtn = document.getElementById('pomo_length');
const shortbtn = document.getElementById('sbreak_length');
const longbtn = document.getElementById('lbreak_length');

workbtn.addEventListener('click', () => {
    length_change(worklength, workbtn);
})
shortbtn.addEventListener('click', () => {
    length_change(short_break, shortbtn);
})
longbtn.addEventListener('click', () => {
    length_change(long_break, longbtn); 
})


// custom timer
// const customInput = document.getElementById('custom-input');
// const customSetBtn = document.getElementById('custom-set');
// const customModal = document.getElementById('custom-modal');

// custom_btn.addEventListener('click', () => {

//     clearActiveState();

//     custom_btn.classList.add('active');
//     customModal.classList.remove('hidden');

//     clearInterval(timer);
//     is_running = false;
//     timer = null;
//     startBtn.textContent = 'Start';
// });

// customSetBtn.addEventListener('click', () => {
//     const minutes = parseInt(customInput.value);
//     if (!isNaN(minutes) && minutes > 0) {
//         modetime = minutes * 60;
//         time_left = modetime;
//         customModal.classList.add('hidden');
//     }
//     timeupdate();
// });

//close window
// customModal.addEventListener('click', (e) => {
//     if (e.target === customModal) {
//         customModal.classList.add('hidden');
//     }
// });



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

let taskmode = 'add';
let selectedFlowTaskId = null;
let taskCache = [];

// Modechange
function updateModeUI() {
    document.body.classList.toggle('delete-mode', taskmode === 'delete');

    addBtn.classList.toggle('active', taskmode === 'add');
    deleteBtn.classList.toggle('active', taskmode === 'delete');   
}

function selectFlowTask(task) {
    if (selectedFlowTaskId === task.id) {
        selectedFlowTaskId = null;
        document.getElementById('flow-task-name').textContent = 'Task: No task selected';
        document.getElementById('flow-task-value').textContent = '';
        document.getElementById('flow-start-btn').disabled = true;

        document.querySelectorAll('.task-item').forEach(item => {
            item.classList.remove('selected');
        });

        return;
    }

    selectedFlowTaskId = task.id;

    document.getElementById('flow-task-name').textContent = `Task: ${task.content}`;
    document.getElementById('flow-task-value').textContent = task.content;
    document.getElementById('flow-start-btn').disabled = false;

    document.querySelectorAll('.task-item').forEach(item => {
        item.classList.toggle('selected', Number(item.dataset.taskId) === selectedFlowTaskId);
    });

    modeswitch('flow');
}

function selectFlowTaskFromList(id) {
    if (taskmode === 'delete') {
        return;
    }

    const task = taskCache.find(item => item.id === id);

    if (task) {
        selectFlowTask(task);
    }
}
// Task management
const getcsrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const addBtn = document.getElementById('add-task-btn');
const deleteBtn = document.getElementById('delete-task-btn');

function redirectToLoginIfNeeded(response) {
    if (response.status === 401 || response.redirected && response.url.includes('/login')) {
        window.location.href = '/login';
        return true;
    }

    return false;
}

addBtn.addEventListener('click', () => {
    taskmode = 'add';
    updateModeUI();
})

deleteBtn.addEventListener('click', () => {
    if (taskmode ==='delete') {
        taskmode = 'add';
    } else {
        taskmode = 'delete';
    }
    updateModeUI();
});

window.onload = function() {
    fetch('/get_tasks')
    .then(response => {
        if (response.status === 401 || response.redirected && response.url.includes('/login')) {
            return { tasks: [] };
        }

        return response.json();
    })
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
        if (redirectToLoginIfNeeded(response)) {
            return;
        }

        return response.json();
    })
    .then(data => {
        if (!data) {
            return;
        }

        renderTasks(data.tasks);
        document.getElementById('task-input').value = '';   
    }); 
});

// Render tasks
function renderTasks(tasks) {
    console.log(tasks);
    console.log(tasks[0]);
    taskCache = tasks;

    if (selectedFlowTaskId !== null && !taskCache.some(task => task.id === selectedFlowTaskId)) {
        selectedFlowTaskId = null;
        document.getElementById('flow-task-name').textContent = 'Task: No task selected';
        document.getElementById('flow-task-value').textContent = '';
        document.getElementById('flow-start-btn').disabled = true;
    }

    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.sort((a, b) => a.status - b.status);
    
    tasks.forEach(task => {
        let className = 'task-item';

        if (task.status == true) {
            className = 'task-item completed';
        }

        if (task.id === selectedFlowTaskId) {
            className += ' selected';
        }

        taskList.innerHTML +=
            `<li class="${className}" id="task-${task.id}" data-task-id="${task.id}" onclick="selectFlowTaskFromList(${task.id})">
                <div class="statusbar"></div>
                <span class="statusbox" onclick="event.stopPropagation(); toggleStatus(${task.id})"></span>
                <span>${task.content}</span>
                <button class="delete-btn" onclick="event.stopPropagation(); deleteTask(${task.id})">-</button>
            </li>`;
    });
    updateModeUI();
}

// Delete task
function deleteTask(id) {
    if (taskmode !== 'delete') {
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


// ============Switch Timer Mode===============
let timermode="pomo";

const flowView = document.getElementById('flowdoro');
const pomoView = document.getElementById('pomodoro');

const flowbtn = document.getElementById('mode-flow');
const pomobtn = document.getElementById('mode-pomo');

function modeswitch(Mode1){
    clearInterval(timer);
    timer = null;
    timermode = Mode1;

    if (timermode === 'flow') {

        flowView.classList.add('active');
        pomoView.classList.remove('active');

        flowbtn.classList.add('active');
        pomobtn.classList.remove('active');

    } else {

        pomoView.classList.add('active');
        flowView.classList.remove('active');

        pomobtn.classList.add('active');
        flowbtn.classList.remove('active');

    }
}

flowbtn.addEventListener('click', () => {
    modeswitch('flow');
});

pomobtn.addEventListener('click', () => {
    modeswitch('pomo');
});
