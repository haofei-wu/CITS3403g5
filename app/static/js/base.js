document.addEventListener('DOMContentLoaded', () => {

    const btn = document.getElementById('menubtn');
    const menu_sidebar = document.getElementById('menusidebar');
    const overlay = document.getElementById('overlay');
    const navAvatarInput = document.getElementById('nav-avatar-input');
    const navAvatarForm = document.getElementById('nav-avatar-form');
    
    btn.addEventListener('click', () => {
        menu_sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    });

    overlay.addEventListener('click', () => {
        menu_sidebar.classList.remove('show');
        overlay.classList.remove('show');
    });

    if (navAvatarInput && navAvatarForm) {
        navAvatarInput.addEventListener('change', () => {
            if (navAvatarInput.files.length > 0) {
                navAvatarForm.submit();
            }
        });
    }
});
