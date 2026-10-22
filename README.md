# CricketBot

Rasa 1.x cricket score chatbot.

## Configuration (secrets)

Secrets are read from environment variables, never from the repo:

- `CRICAPI_KEY` (actions.py, cricapi.com)
- `FB_VERIFY_TOKEN`, `FB_APP_SECRET`, `FB_PAGE_ACCESS_TOKEN` (credentials.yml, Facebook channel; Rasa expands `${VAR}`)

Copy `.env.example` to `.env`, fill it in, and export it (`set -a; . ./.env; set +a`) before
`rasa run` / `rasa run actions`. `.env` is git-ignored. Keys previously committed to git
history must be rotated at the provider and not reused.
