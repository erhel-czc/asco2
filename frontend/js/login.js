const local_API_BASE = window.location.origin;

document.querySelector("form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const submitBtn = this.querySelector("button[type=submit]");
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    submitBtn.disabled = true;
    submitBtn.textContent = "Connexion en cours...";

    try {
        const response = await fetch(`${local_API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            // The cookie is now set by the server, so a simple redirect is enough.
            window.location.href = "/";
            return;
        }

        const payload = await response.json().catch(() => null);
        const message = payload.detail || "Une erreur est survenue. Veuillez réessayer.";

        showError(message);

    } catch {
        showError("Impossible de contacter le serveur. Vérifiez votre connexion.");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Se connecter";
    }
});

function showError(message) {
    let banner = document.getElementById("login-error");

    if (!banner) {
        banner = document.createElement("p");
        banner.id = "login-error";
        banner.setAttribute("role", "alert");
        banner.style.color = "var(--color-error, #c0392b)";
        banner.style.marginTop = "0.5rem";
        document.querySelector("form").prepend(banner);
    }
    
    banner.textContent = message;
}
