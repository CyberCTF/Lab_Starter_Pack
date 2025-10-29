# Maintainers Guide (Private)

This document is for maintainers and automated assistants only. Do NOT expose its contents to players. Player-facing materials must follow Help Content Guidelines (no hints, no solutions).

## Flag Location and Retrieval (Template)

- Flag source: database row in `dev_data75.flags` table (example) or app secret configured for tests.
- Expected flag value: defined in `.ctf/FLAG.md` and referenced by tests.

## End-to-End Steps to Validate and Extract the Flag

1) Environment readiness
- Ensure Docker Desktop/engine is running.
- From repo root, validate both compose files:
  - `docker compose up -d --build`
  - `docker compose -f build/docker-compose.dev.yml up -d --build`

2) Health verification
- Web healthcheck: `curl -fsS http://localhost:${WEB_PORT:-3206}/health`
- DB healthcheck is handled by compose (`mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD"`).

3) Database initialization sanity
- Check init order and privileges (user then GRANT; separate global vs DB grants).
- Connect: `docker compose exec database mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"`

4) Run tests including flag extraction
- `pytest -q`
- If markers exist: `pytest -q -m flag_extraction`

5) Manual exploitation path (if tests fail)
- Identify vulnerable endpoint (search in `build/web/src/` for SQL queries or inputs feeding SQL).
- Use controlled payload to enumerate tables (e.g., UNION SELECT or parameter misuse depending on stack).
- Locate the flag-bearing record or secret and extract the exact value required by tests.

6) UI conformance check (non-player-facing)
- Confirm shadcn-like layout, dark mode, and absence of warnings/disclaimers.

## Notes
- Never add hints into UI, README, or any player-visible page.
- All corrections must respect `.cursor/rules` (compose parity, MySQL healthcheck, Apache Listen, etc.).
- Record outcomes in `.ctf/REVIEW.md`; produce `.ctf/GOOD.md` only when all tests pass.
