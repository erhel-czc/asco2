const local_API_BASE = window.location.origin;
const statusNode = document.getElementById("association-reports-status");
const gridNode = document.getElementById("association-reports-grid");
const titleNode = document.getElementById("association-reports-title");
const subtitleNode = document.getElementById("association-reports-subtitle");
const pathParts = window.location.pathname.split("/");
const associationId = Number(pathParts[2]);

document.getElementById("btn-add-report").addEventListener("click", (event) => {
    event.preventDefault();
    // TODO: ouvrir modal ou naviguer vers formulaire d'ajout de bilan.
    alert("Fonctionnalité à venir : ajouter un bilan d'association.");
});

async function fetchMyAssociations() {
    const response = await fetch(`${local_API_BASE}/associations/mine`, {
        method: "GET",
        credentials: "same-origin",
    });

    if (response.status === 401) {
        window.location.href = "/login";
        return null;
    }

    if (!response.ok) {
        throw new Error("failed_to_load_associations");
    }

    return response.json();
}

async function fetchAssociationReports() {
    const response = await fetch(`${local_API_BASE}/associations/${associationId}/reports`, {
        method: "GET",
        credentials: "same-origin",
    });

    if (response.status === 401) {
        window.location.href = "/login";
        return null;
    }

    if (response.status === 403) {
        statusNode.textContent = "Vous n'avez pas accès à cette association.";
        return [];
    }

    if (!response.ok) {
        throw new Error("failed_to_load_reports");
    }

    return response.json();
}

function renderReports(reports) {
    gridNode.innerHTML = "";
    statusNode.textContent = "";

    if (!Array.isArray(reports) || reports.length === 0) {
        const empty = document.createElement("p");
        empty.className = "dashboard-empty";
        empty.textContent = "Aucun bilan n'a encore été ajouté pour cette association.";
        gridNode.appendChild(empty);
        return;
    }

    reports.forEach((reportItem) => {
        const tile = document.createElement("div");
        tile.className = "association-tile";

        const total = (
            reportItem.food_carbon_footprint
            + reportItem.transport_carbon_footprint
            + reportItem.stuff_carbon_footprint
        ).toFixed(2);

        tile.innerHTML = `
            <span class="association-tile__name">${reportItem.report_title}</span>
            <span class="association-tile__description">Bilan #${reportItem.id}</span>
            <span class="association-tile__role">Empreinte estimée : ${total} kgCO₂e</span>
        `;

        gridNode.appendChild(tile);
    });
}

async function loadAssociationReportsPage() {
    if (!Number.isFinite(associationId)) {
        statusNode.textContent = "Association invalide.";
        return;
    }

    const associations = await fetchMyAssociations();

    if (associations === null) {
        return;
    }

    const currentAssociation = associations.find((association) => association.id === associationId);

    if (!currentAssociation) {
        statusNode.textContent = "Association introuvable dans votre tableau de bord.";
        return;
    }

    titleNode.textContent = `Association : ${currentAssociation.association_name}`;
    subtitleNode.textContent = "Retrouvez les bilans de cette association.";

    const reports = await fetchAssociationReports();

    if (reports === null) {
        return;
    }

    renderReports(reports);
}

loadAssociationReportsPage().catch(() => {
    statusNode.textContent = "Impossible de charger les bilans de cette association.";
});
