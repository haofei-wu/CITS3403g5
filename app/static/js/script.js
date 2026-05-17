// Timer
// Get elements
const mode_btns = document.querySelectorAll('.mode-btn:not(#custom-btn)');

const timerDisplay = document.getElementById('simple-timer');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');

// Store timer interval id
let timer= null;

let is_running = false;

// Get timer lengths from HTML
let worklength = document.getElementById('pom-worklength').textContent;
let short_break = document.getElementById('pom-short-break').textContent;
let long_break = document.getElementById('pom-long-break').textContent;

let modetime = worklength * 60;

let time_left = modetime;



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

// clear active state
function clearActiveState() {
    mode_btns.forEach(btn => btn.classList.remove('active'));
    // custom_btn.classList.remove('active');
}

// change timer length when mode button is clicked
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

function getLocal() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

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
    fetch(`/get_tasks?taskdate=${getLocal()}`)
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
        body: JSON.stringify({
            task: taskInput,
            taskdate: getLocal()
        })
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

    fetch(`/delete_tasks/${id}?taskdate=${getLocal()}`, {
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
    fetch(`/toggle_status/${id}?taskdate=${getLocal()}`, {
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



// ============Search Functionality===============
let taskHistory = [];
// Store Fuse search object for task search
let taskFuse = null;

// Fetch task history for search suggestions
fetch("/task_history")
    .then(res => {
        if (res.status === 401 || res.redirected && res.url.includes('/login')) {
            return;
        }

        return res.json();
    })
    .then(data => {
        if (!data) {
            return;
        }

        taskHistory = data.tasks;

        // Create a fuse search 
        taskFuse = new Fuse(taskHistory, {
            keys: ["content"],
            threshold: 0.35
        });
    });

// Get task input element
const taskInput = document.getElementById("task-input");

//listen for typing input element
taskInput.addEventListener("input", () => {

    const query = taskInput.value.trim();

    // Hide suggestions if query is empty
    if (!query || !taskFuse) {
        hideSuggestions();
        return;
    }

    // Keep top 5 results
    const results = taskFuse.search(query).slice(0, 5);
    renderSuggestions(results.map(r => r.item));
});

// Fill input
function selectSuggestion(task) {
    taskInput.value = task.content;
    hideSuggestions();
}

function hideSuggestions() {
    const container = document.getElementById("task-suggestions");
    container.innerHTML = "";
    container.classList.remove("show");
}

function renderSuggestions(tasks) {
    const container = document.getElementById("task-suggestions");
    container.innerHTML = "";
    container.classList.toggle("show", tasks.length > 0);

    tasks.forEach(task => {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "task-suggestion";
        item.textContent = task.content;
        item.addEventListener("click", () => selectSuggestion(task));
        container.appendChild(item);
    });
}
