const local_API_BASE = window.location.origin;
const statusNode = document.getElementById("dashboard-status");
const gridNode = document.getElementById("associations-grid");

document.getElementById("btn-add-association").addEventListener("click", () => {
    // TODO: ouvrir modal ou naviguer vers formulaire d'ajout
    alert("Fonctionnalité à venir : rejoindre ou créer une association.");
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
        const tile = document.createElement("div");
        tile.className = "association-tile";

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