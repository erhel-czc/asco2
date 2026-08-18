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
});