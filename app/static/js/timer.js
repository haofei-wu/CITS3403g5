let livetime = {}
    
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

    
});

document.getElementById("end-btn").addEventListener("click", function() {
    // console.log("working")
    document.getElementById("end-btn").style.display = "none";
    document.getElementById("start-btn").style.display = "block";
    clearInterval(timerrefresh);
    console.log("killed timer");

    // set interval to update timer displayer every second using setinterval
});

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

