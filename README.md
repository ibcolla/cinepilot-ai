# CinePilot AI

CinePilot AI is a film production continuity intelligence project designed to help production teams catch issues such as wardrobe mismatches, missing props, scene inconsistencies, and continuity errors before they become costly post-production problems.

This repository contains a working demo focused on a production continuity workflow for a single Scene 12 use case. The application combines a web frontend, a FastAPI backend, Gemini-based reasoning, and ClickHouse-backed production data access through an MCP-style integration layer.

## What CinePilot AI is

CinePilot AI is an autonomous continuity supervisor for film and video production. It helps a production team review a take, compare it against an approved standard, and identify whether the scene remains consistent with the approved production record.

The goal is not to replace editorial judgment or a production department, but to give teams a faster and more systematic way to catch continuity risks early in the process.

## The production continuity problem it solves

In production, small continuity mistakes can create major downstream problems:

- wardrobe changes between takes that are not intended
- props appearing or disappearing between shots
- lighting or environment inconsistencies
- scene context drift from the approved production plan

These issues often require manual review across many shots and takes. CinePilot AI brings structure to that process by turning those observations into a repeatable continuity analysis workflow.

## Scene 12 use case

The current demonstration is centered on a specific production scenario: Scene 12, an office-arrival sequence. In this example, the system is evaluating whether a take deviates from the approved production standard.

The demo intentionally focuses on a small, high-clarity example to show how continuity violations can be surfaced in production terms:

- wardrobe discrepancy
- prop omission
- approved take comparison
- corrective action recommendation

This represents a realistic production review scenario while keeping the demo easy to understand and present.

## Current application capabilities

The current project includes a web application with the following flows:

- a dashboard overview for the production continuity workflow
- a Scene 12 analysis screen
- a live analysis workflow that calls the backend analysis endpoint
- a continuity review view that surfaces detected issues and approved standards
- a production memory view that summarizes approved decisions

The backend exposes health and analysis endpoints and is designed to evaluate a scene against production context and the approved standard. The front end communicates with the backend over HTTP and presents the result in a production-oriented interface.

## High-level architecture

The project is organized around a simple layered pattern:

1. Frontend: Next.js app for presentation and user navigation
2. Backend: FastAPI service that exposes REST endpoints
3. Agent/orchestrator layer: reasoning and orchestration logic
4. MCP / ClickHouse layer: production data context and decision retrieval
5. Gemini model layer: analysis and production recommendation generation

This architecture is intentionally lightweight and suitable for a demo environment focused on continuity analysis rather than a full production-scale platform.

## Frontend and backend

### Frontend

The frontend lives under `frontend/` and uses Next.js with React.

It includes pages for:

- Dashboard
- Scene 12
- Continuity review
- Production Memory

It is designed to interact with the backend at `http://localhost:8000` by default, using the API client under `frontend/src/services/api.ts`.

### Backend

The backend entry point is `api.py`, implemented with FastAPI.

Key responsibilities include:

- health checks
- agent status reporting
- scene analysis requests
- orchestration of continuity analysis logic
- JSON responses that can be consumed by the frontend

The API is intended to provide a consistent response model for scene analysis results.

## MCP and ClickHouse

The orchestrator layer in `agents/orchestrator/agent_mcp.py` integrates production data access with an MCP-style workflow and ClickHouse-backed queries. In the current demo, ClickHouse data is used as a production record source for approved take decisions and scene context. The orchestrator then passes that information alongside the user request to the Gemini model for continuity reasoning.

This means the agent is not purely static analysis; it is designed to compare observed issues against production decisions and approved standards stored in the data layer.

## Repository structure

Key areas of the project include:

- `api.py` — FastAPI app and backend endpoints
- `agents/` — orchestrator and analysis agents
- `clickhouse/` — schema and seed scripts for the demo data model
- `frontend/` — Next.js UI
- `docs/` — project documentation and design material
- `tests/` — validation and workflow checks
- `demo/` and seed scripts — scenario and sample data for the production continuity use case

## How to run the application

### Prerequisites

- Python 3.12+
- Node.js and npm
- access to the required environment variables for Gemini and related services
- a local backend environment that can serve the FastAPI API

### Backend

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If this project is using the configured dependency metadata in `pyproject.toml`, install the project dependencies with your preferred Python environment workflow, then run:

```bash
python3 api.py
```

This launches the backend on port `8000`.

### Frontend

From the `frontend/` directory:

```bash
npm install
npm run dev -- --hostname 0.0.0.0 --port 3000
```

Then open:

```text
http://localhost:3000
```

The frontend defaults to the backend at `http://localhost:8000` unless a different `NEXT_PUBLIC_API_BASE_URL` is configured.

## How to run tests

Python tests are defined under `tests/` and are configured through `pyproject.toml`.

Run them with:

```bash
pytest
```

For the frontend, use the app’s standard Next.js tooling when needed:

```bash
cd frontend
npm run build
```

This repository also contains scenario-oriented validation scripts and demo-oriented test files focused on the MCP and ClickHouse workflow.

## Current demo status

The current repository is a working demo for a production continuity workflow, with the main demonstrable flow centered on the Scene 12 scenario.

The demo currently includes:

- dashboard and navigation pages
- a Scene 12 analysis interface
- continuity review output
- production memory / approved decision view
- backend endpoints for readiness, status, and analysis

The demo status is best described as a presentable proof-of-concept focused on a concrete continuity issue and its decision flow.

## Known limitations

This project is intentionally scoped and should be understood as a demo and workflow prototype rather than a production-ready platform.

Key limitations include:

- the primary scenario is a single, focused use case (Scene 12)
- some screens rely on fixture/demo data to illustrate the experience
- live analysis is gated by environment configuration and external service availability
- data access and agent behavior may depend on local credentials and service setup
- the project is not intended to be deployed without validating the required environment configuration and service availability

Because this is a demo, the product memory and continuity screens should be viewed as illustrative examples of the expected user experience, not a complete live production database.

## Final demo video

Final demo (Scene 12): https://youtu.be/XkPYM1uuA4s?si=QbpznOp_qJc_BnAe

## Project goals

CinePilot AI is meant to demonstrate how AI can support production continuity supervision by:

- making continuity issues visible earlier
- comparing a current take to an approved production standard
- surfacing actionable recommendations
- creating a more structured production decision trail

This keeps the project aligned with its original purpose: accelerating the review of continuity-critical moments in a film production pipeline.

## License

This project is distributed under the MIT license.
