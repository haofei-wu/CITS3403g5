
let livetime = {}
let timerrefresh = null;

// source venv/bin/activate
async function commitSessionTimes() {
    const selectedTask = document.querySelector("#flow-task-value").textContent;

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
        sessiondate: new Date().toISOString().split('T')[0]
    })
});
};
    // we want user click timer start, click again end, and know how much time elapsed
    // store start and end time in external object
    // in external object minus end from start on the second click
    // return difference
function formatMs(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

    // formatTime(125000); // "02:05" 
    
document.getElementById("flow-start-btn").addEventListener("click", function() {
    if (!document.querySelector("#flow-task-value").textContent) {
        return;
    }

    // keytimes.startTime = Date.now()
    // console.log("working")
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
    // console.log("working")
    document.getElementById("flow-end-btn").style.display = "none";
    document.getElementById("flow-start-btn").style.display = "block";
    clearInterval(timerrefresh);
    console.log("killed timer");
    commitSessionTimes();
    document.getElementById("flow-task-name").style.display = "none";
    document.getElementById("restTime").style.display = "flex";
    document.querySelector("#timer-display").innerHTML = formatMs((livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML);
    countdownTimer();
    //countdown ment.getElementById("restTime").innerHTML = formatTime((livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML);
    
    // set interval to update timer displayer every second using setinterval
});
//countdown 




//countdown timer -> date.now() + resttime
// set interval to update timer display every second until, date.now() = date.now() + resttime

// "flow-end-btn".addEventListener("click", timeElapsed(currentTime)
//     let timepassed = Date.now() - startTime;
//     return timepassed;
// }

