const burger = document.querySelector('.burger');
const nav = document.querySelector('.navbar nav');

burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
});

async function checkAuthentication() {
    try {
        const response = await fetch('/auth/me', { credentials: 'same-origin' });
        return response.ok && (await response.json()) != null;
    } catch (error) {
        console.error('Error checking authentication:', error);
        return false;
    }
}

checkAuthentication().then(isAuthenticated => {
    const loginBtn = document.querySelector('.nav-login');
    loginBtn.textContent = isAuthenticated ? 'Tableau de bord' : 'Connexion';
    loginBtn.href = isAuthenticated ? '/dashboard' : '/login';

    if (isAuthenticated) {
        const group = document.createElement('div');
        group.className = 'nav-user-group';

        loginBtn.parentNode.replaceChild(group, loginBtn);
        group.appendChild(loginBtn);

        const logoutBtn = document.createElement('a');
        logoutBtn.className = 'nav-login nav-logout';
        logoutBtn.innerHTML = `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" aria-hidden="true">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12h-9.5m7.5 3l3-3-3-3m-5-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2h5a2 2 0 002-2v-1"/>
        </svg>`;
        logoutBtn.setAttribute('aria-label', 'Logout');
        logoutBtn.href = '#';

        group.appendChild(logoutBtn);

        logoutBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            try {
                const response = await fetch('/auth/logout',
                    { method: 'POST', credentials: 'same-origin' });

                if (response.ok) {
                    window.location.href = '/';

                } else {
                    console.error('Logout failed:', response.statusText);
                }

            } catch (error) {
                console.error('Error during logout:', error);
            }
        });
    }
});