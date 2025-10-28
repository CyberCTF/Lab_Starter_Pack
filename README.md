# Lab Starter Pack

Authoring space for a complete CyberCTF lab. Implement all lab code inside `build/` and tests in `tests/`. Use `.cursor/rules/` as the single source of truth for requirements.

## Structure

- `build/`
  - `docker-compose.dev.yml` (dev compose)
  - `web/` (or `api/`, `database/`) — each with a `Dockerfile` and `src/`
  - `.github/workflows/publish.yml` (optional CI publish)
  - `config/` (optional shared config)
- `tests/` — pytest suite validating Docker health, ports, and app functionality
- `docker-compose.yml` (root-level production compose)
- `.ctf/` — planning/metadata artefacts (SCENARIO, FLAG, metadata, timing)

## Cursor Guidance

1. Follow `.cursor/rules/apps/development/*` for lab creation and Docker details.
2. Follow `.cursor/rules/apps/run/*` for compose, env vars, networks, and ports.
3. Follow `.cursor/rules/apps/review/*` for QA, timing, and documentation hygiene.
4. Generate only within `build/` and `tests/`; store transient artefacts in `.ctf/`.

## Critical Rules (high-signal)

- Compose V2: no `version:` key; ports are env-driven; add healthchecks; keep dev/prod parity.
- Web server must listen on the assigned internal port (e.g., Apache `Listen 3206` + VirtualHost).
- DB init: numbered SQL files; create user before GRANT; separate DB vs global privileges.
- Package managers must match base image (Debian=apt-get, Alpine=apk, Oracle=microdnf).
- Quote passwords with special characters in Compose `environment:`.

## Getting Started

1. Create `build/web/` with a minimal app and `Dockerfile`.
2. Add `build/docker-compose.dev.yml` and root `docker-compose.yml` with env-driven ports.
3. If needed, add `build/database/` with `init/01-*.sql`, `02-*.sql`, etc.
4. Write tests in `tests/` to assert container health and basic functionality.


