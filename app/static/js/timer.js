
let livetime = {}

// source venv/bin/activate
const getcsrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
async function commitSessionTimes() {           
    const response = await fetch("/sessiontimes", {
    headers: {
        "Content-Type": "application/json",
       "X-CSRFToken": getcsrfToken
    },
    method: "POST",
    body: JSON.stringify({
        startTime: livetime.startTime,
        endTime: livetime.endTime,
        task: document.querySelector("#task-input").value,
        sessiondate: new Date().toISOString().split('T')[0]
    })
});
};
    // we want user click timer start, click again end, and know how much time elapsed
    // store start and end time in external object
    // in external object minus end from start on the second click
    // return difference
function formatTime(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

    // formatTime(125000); // "02:05" 
    
document.getElementById("start-btn").addEventListener("click", function() {
    // keytimes.startTime = Date.now()
    // console.log("working")
    document.getElementById("start-btn").style.display = "none";
    document.getElementById("end-btn").style.display = "block";
    livetime.startTime = Date.now()
    // Every 1000 ms, take current time as end time, and subtact start time from it
     timerrefresh = setInterval(() => {
        livetime.endTime = Date.now();
        let timeElapsed = (livetime.endTime - livetime.startTime);
        document.querySelector("#timer-display").innerHTML = formatTime(timeElapsed)}, 1000);
     }, 1000);

    




function countdownTimer() {
    let resttime = Date.now() + (livetime.startTime - livetime.endTime + 1200000 )/document.getElementById("flow-restratio").innerHTML;
    let countdown = setInterval(() => {     
            if (Date.now() < resttime)   {
                document.querySelector("#timer-display").innerHTML = formatTime(resttime - Date.now()) + "s remaining";
            } else {
                clearInterval(countdown);
                document.querySelector("#timer-display").innerHTML = "00:00";
                return;
            }
    }, 1000);
}


document.getElementById("end-btn").addEventListener("click", function() {
    // console.log("working")
    document.getElementById("end-btn").style.display = "none";
    document.getElementById("start-btn").style.display = "block";
    clearInterval(timerrefresh);
    console.log("killed timer");
    commitSessionTimes();
    document.getElementById("restTime").style.display = "flex";
    document.querySelector("#timer-display").innerHTML = formatTime((livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML) + "s remaining";
    countdownTimer();
    //countdown ment.getElementById("restTime").innerHTML = formatTime((livetime.endTime - livetime.startTime)/document.getElementById("flow-restratio").innerHTML);
    
    // set interval to update timer displayer every second using setinterval
});
//countdown 




//countdown timer -> date.now() + resttime
// set interval to update timer display every second until, date.now() = date.now() + resttime



fetch("/sessiontimes", {
    method: "POST",
    body: JSON.stringify({
        startTime: livetime.startTime,
        endTime: livetime.endTime,
    })
})


// "end-btn".addEventListener("click", timeElapsed(currentTime)
//     let timepassed = Date.now() - startTime;
//     return timepassed;
// }

