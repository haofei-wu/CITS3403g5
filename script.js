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