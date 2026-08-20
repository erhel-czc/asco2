const local_API_BASE = window.location.origin;
const statusNode = document.getElementById("dashboard-status");
const gridNode = document.getElementById("associations-grid");
const associationModal = document.getElementById("association-modal");
const associationForm = document.getElementById("association-form");
const associationFormError = document.getElementById("association-form-error");

document.getElementById("btn-add-association").addEventListener("click", (event) => {
    event.preventDefault();
    associationForm.reset();
    associationFormError.textContent = "";
    associationModal.showModal();
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", () => associationModal.close());
});

associationModal.addEventListener("click", (event) => {
    if (event.target === associationModal) associationModal.close();
});

associationForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitButton = associationForm.querySelector("button[type=submit]");
    submitButton.disabled = true;
    associationFormError.textContent = "";

    try {
        const userResponse = await fetch(`${local_API_BASE}/auth/me`, { credentials: "same-origin" });
        if (userResponse.status === 401) {
            window.location.href = "/login";
            return;
        }
        if (!userResponse.ok) throw new Error("failed_to_load_user");
        const user = await userResponse.json();
        const response = await fetch(`${local_API_BASE}/associations`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify({
                association_name: associationForm.elements.association_name.value.trim(),
                association_description: associationForm.elements.association_description.value.trim(),
                initial_admin_id: user.id,
            }),
        });
        if (!response.ok) throw new Error("failed_to_create_association");
        associationModal.close();
        await loadAssociations();
    } catch {
        associationFormError.textContent = "Impossible de créer l’association pour le moment.";
    } finally {
        submitButton.disabled = false;
    }
});

async function loadAssociations() {
    const response = await fetch(`${local_API_BASE}/associations/mine`, {
        method: "GET",
        credentials: "same-origin",
    });

    if (response.status === 401) {
        window.location.href = "/login";
        return;
    }

    if (!response.ok) {
        throw new Error("failed_to_load_associations");
    }

    const associations = await response.json();
    renderAssociations(associations);
}

function renderAssociations(associations) {
    gridNode.innerHTML = "";
    statusNode.textContent = "";

    if (!Array.isArray(associations) || associations.length === 0) {
        const empty = document.createElement("p");
        empty.className = "dashboard-empty";
        empty.textContent = "Vous n'êtes membre d'aucune association pour le moment.";
        gridNode.appendChild(empty);
        return;
    }

    associations.forEach((association) => {
        const tile = document.createElement("a");
        tile.className = "association-tile";
        tile.href = `/association/${association.id}`;

        const role = association.is_admin ? "Admin" : "Membre";
        tile.innerHTML = `
            <span class="association-tile__name">${association.association_name}</span>
            <span class="association-tile__description">${association.association_description}</span>
            <span class="association-tile__role">Rôle : ${role}</span>
        `;

        gridNode.appendChild(tile);
    });
}

loadAssociations().catch(() => {
    statusNode.textContent = "Impossible de charger vos associations pour le moment.";
});