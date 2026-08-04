const burger = document.querySelector('.burger');
const nav = document.querySelector('.navbar nav');

burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
});
