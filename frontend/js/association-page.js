const local_API_BASE = window.location.origin;
const statusNode = document.getElementById("association-reports-status");
const gridNode = document.getElementById("association-reports-grid");
const titleNode = document.getElementById("association-reports-title");
const subtitleNode = document.getElementById("association-reports-subtitle");
const reportModal = document.getElementById("report-modal");
const reportForm = document.getElementById("report-form");
const reportFormError = document.getElementById("report-form-error");
const pathParts = window.location.pathname.split("/");
const associationId = Number(pathParts[2]);

document.getElementById("btn-add-report").addEventListener("click", (event) => {
    event.preventDefault();
    reportForm.reset();
    reportFormError.textContent = "";
    reportModal.showModal();
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", () => reportModal.close());
});

reportModal.addEventListener("click", (event) => {
    if (event.target === reportModal) reportModal.close();
});

reportForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitButton = reportForm.querySelector("button[type=submit]");
    submitButton.disabled = true;
    reportFormError.textContent = "";

    try {
        const response = await fetch(`${local_API_BASE}/associations/${associationId}/reports`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify({
                id: 0,
                report_title: reportForm.elements.report_title.value.trim(),
                report_description: reportForm.elements.report_description.value.trim(),
                food_carbon_footprint: 0,
                transport_carbon_footprint: 0,
                stuff_carbon_footprint: 0,
            }),
        });
        if (response.status === 401) {
            window.location.href = "/login";
            return;
        }
        if (response.status === 403) throw new Error("forbidden");
        if (!response.ok) throw new Error("failed_to_create_report");
        reportModal.close();
        await loadAssociationReportsPage();
    } catch (error) {
        reportFormError.textContent = error.message === "forbidden"
            ? "Vous n’avez pas accès à cette association."
            : "Impossible de créer le bilan pour le moment.";
    } finally {
        submitButton.disabled = false;
    }
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
            <span class="association-tile__description">${reportItem.report_description}</span>
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
