
let livetime = {}
let timerrefresh = null;


async function commitSessionTimes() {
    const selectedTask = document.querySelector("#flow-task-value").textContent;
    //commits the session times to the database
    const response = await fetch("/sessiontimes", {
    headers: {
        "Content-Type": "application/json",
       "X-CSRFToken": getcsrfToken
    },
    method: "POST",
    body: JSON.stringify({
        startTime: livetime.startTime,
        endTime: livetime.endTime,
        task: selectedTask,
        sessiondate: getLocal()
    })
});
};

//formats milliseconds to minutes and seconds for display
function formatMs(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

    
document.getElementById("flow-start-btn").addEventListener("click", function() {
    if (!document.querySelector("#flow-task-value").textContent) {
        return;
    }

    document.getElementById("flow-task-name").style.display = "flex";
    document.getElementById("restTime").style.display = "none";
    document.getElementById("flow-start-btn").style.display = "none";
    document.getElementById("flow-end-btn").style.display = "block";
    livetime.startTime = Date.now()
    // Every 1000 ms, take current time as end time, and subtact start time from it
     timerrefresh = setInterval(() => {
        livetime.endTime = Date.now();
        let timeElapsed = (livetime.endTime - livetime.startTime);
        document.querySelector("#timer-display").innerHTML = formatMs(timeElapsed)}, 1000);
     }, 1000);


function countdownTimer() {
    //starts a countdown timer based on the rest time and the flow rest ratio
    let resttime = Date.now() + (livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML;
    let countdown = setInterval(() => {     
            if (Date.now() < resttime)   {
                document.querySelector("#timer-display").innerHTML = formatMs(resttime - Date.now());
            } else {
                clearInterval(countdown);
                document.querySelector("#timer-display").innerHTML = "00:00";
                document.getElementById("restTime").style.display = "none";
                document.getElementById("flow-task-name").style.display = "flex";
                return;
            }
    }, 1000);
}


document.getElementById("flow-end-btn").addEventListener("click", function() {
    //ends the timer and commits the session times to the database
    document.getElementById("flow-end-btn").style.display = "none";
    document.getElementById("flow-start-btn").style.display = "block";
    clearInterval(timerrefresh);
    commitSessionTimes();
    document.getElementById("flow-task-name").style.display = "none";
    document.getElementById("restTime").style.display = "flex";
    document.querySelector("#timer-display").innerHTML = formatMs((livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML);
    countdownTimer();
});

// converts UTC time to local time
function getLocal() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}
