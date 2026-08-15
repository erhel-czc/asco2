const local_API_BASE = window.location.origin;

document.querySelector("form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const password = document.getElementById("password");
    const confirm = document.getElementById("password-confirm");

    if (password.value !== confirm.value) {
        confirm.classList.add("error");
        confirm.setCustomValidity("Les mots de passe ne correspondent pas.");
        confirm.reportValidity();
        return;
    }

    confirm.classList.remove("error");
    confirm.setCustomValidity("");

    const email = document.getElementById("email").value.trim();
    const firstname = document.getElementById("firstname").value.trim();
    const lastname = document.getElementById("lastname").value.trim();
    const username = `${firstname} ${lastname}`;

    const submitBtn = this.querySelector("button[type=submit]");
    submitBtn.disabled = true;
    submitBtn.textContent = "Création en cours…";

    if (window.location.protocol !== "https:" && window.location.hostname !== "localhost") {
        showError("Pas de connexion ou connexion non sécurisée.");
        submitBtn.disabled = false;
        submitBtn.textContent = "Créer mon compte";
        return;
    }

    try {
        const response = await fetch(`${local_API_BASE}/users`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username,
                email,
                password: password.value,
            }),
        });

        const requestSucceeded = response.ok;

        if (requestSucceeded) {
            // DO SOMETHING ON SUCCESS
            return;
        }

        const fallbackMessage = "Une erreur est survenue. Veuillez réessayer.";
        let errorMessage = fallbackMessage;

        const errorPayload = await response.json().catch(() => null);

        if (
            errorPayload &&
            typeof errorPayload.detail === "string" &&
            errorPayload.detail.trim() !== ""
        ) {
            errorMessage = errorPayload.detail;
        }

        showError(errorMessage);
    } catch {
        showError("Impossible de contacter le serveur. Vérifiez votre connexion.");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Créer mon compte";
    }
});

function showError(message) {
    let banner = document.getElementById("signup-error");
    if (!banner) {
        banner = document.createElement("p");
        banner.id = "signup-error";
        banner.setAttribute("role", "alert");
        banner.style.color = "var(--color-error, #c0392b)";
        banner.style.marginTop = "0.5rem";
        document.querySelector("form").prepend(banner);
    }
    banner.textContent = message;
}
