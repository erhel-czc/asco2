# Copilot Instructions for asco2

This project builds a carbon-footprint web application for associations in a French context.

## Product Direction

- Prioritize clarity and simplicity over advanced UX complexity.
- Keep calculations traceable: each result must map to factor source and unit.
- Communicate uncertainty: outputs are estimates, not audited accounting statements.

## Technical Direction

- Backend framework: FastAPI.
- Frontend stack: vanilla HTML/CSS/JS.
- Prefer explicit, typed Pydantic schemas for request/response models.
- Keep external API access isolated in service clients.

## Data Integration Rules

- Prefer ADEME-compatible public factors and APIs.
- If using Impact CO2 endpoints, isolate them in a dedicated adapter/client.
- Always normalize units before calculations.
- Store or return factor metadata (source, version/date, endpoint).

## Code Quality Rules

- Add tests for new calculation logic.
- Avoid hidden constants in formulas; keep constants centralized.
- Validate all user inputs strictly.
- Keep side effects (I/O, API calls) separate from pure calculation functions.

## Security and Privacy

- Do not log secrets.
- Keep API keys in environment variables.
- Do not collect personal data unless required by a clearly documented feature.
