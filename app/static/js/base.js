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