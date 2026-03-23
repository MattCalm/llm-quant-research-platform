# Azure Deployment Readiness (MVP Scaffold)

## Target runtime
- Azure App Service (container) or Azure Container Apps

## Required environment variables
- `LQRP_ENVIRONMENT=prod`
- `LQRP_LOG_LEVEL=INFO`
- `LQRP_LLM_PROVIDER=mock` (switch to `openai` when integrated)
- `LQRP_OPENAI_API_KEY=<secret>`

## Startup command
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## TODO (phase1)
- Add auth and rate limiting
- Add secrets integration with Key Vault
- Add telemetry and alerting
