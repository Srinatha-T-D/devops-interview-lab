# Contributing to the Order API lab

## Workflow

1. Start from an up-to-date `main` branch.
2. Create one focused branch using `<type>/<short-description>`; for example, `feat/add-order-filter` or `fix/database-timeout`.
3. Keep commits small and use a clear Conventional Commit-style message, such as `feat: add order status filter`.
4. Open a pull request. Do not push directly to `main`.

## Before requesting review

Run the local service and validate the customer path:

```powershell
docker compose up --build -d
curl.exe -i http://localhost:8080/livez
curl.exe -i http://localhost:8080/readyz
curl.exe http://localhost:8080/api/v1/orders
docker compose down
```

## Pull-request description

State the user impact, the implementation approach, validation evidence, configuration or infrastructure changes, and rollback plan. Never include secrets, access tokens, private keys, or a real `.env` file in a commit or pull request.
