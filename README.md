# Zoho Recruit ATS Integration Microservice

Python + Serverless microservice that exposes a unified API and connects to Zoho Recruit.

## Endpoints

1. GET /jobs
2. POST /candidates
3. GET /applications?job_id=...

## Standard Response Shapes

### GET /jobs
```json
{
  "data": [
    {
      "id": "string",
      "title": "string",
      "location": "string",
      "status": "OPEN|CLOSED|DRAFT",
      "external_url": "string"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "count": 1,
    "has_next": false
  }
}
```

### POST /candidates
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "resume_url": "string",
  "job_id": "string"
}
```

### GET /applications
```json
{
  "data": [
    {
      "id": "string",
      "candidate_name": "string",
      "email": "string",
      "status": "APPLIED|SCREENING|REJECTED|HIRED"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "count": 1,
    "has_next": false
  }
}
```

## What you already have

You shared:
- ZOHO_CLIENT_ID
- ZOHO_CLIENT_SECRET

These are already prefilled in .env.template.

## What you still need manually

1. Generate ZOHO_REFRESH_TOKEN using Zoho OAuth flow.
2. Get ZOHO_ORG_ID from your Zoho Recruit org URL/settings.
3. Create one test Job Opening and keep its job_id.

## Generate Refresh Token

Open this in browser (replace CLIENT_ID):

```text
https://accounts.zoho.in/oauth/v2/auth?scope=ZohoRecruit.modules.ALL,ZohoRecruit.settings.ALL,ZohoRecruit.users.ALL&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=http://localhost:3000/callback
```

After consent, you get redirected with ?code=...

Exchange code for tokens:

```powershell
Invoke-RestMethod -Method Post -Uri "https://accounts.zoho.in/oauth/v2/token" -Body @{
  grant_type="authorization_code"
  client_id="YOUR_CLIENT_ID"
  client_secret="YOUR_CLIENT_SECRET"
  redirect_uri="http://localhost:3000/callback"
  code="PASTE_CODE_HERE"
}
```

Copy refresh_token from response.

## Local Setup

```powershell
copy .env.template .env
```

Fill missing values in .env:

```env
ZOHO_REFRESH_TOKEN=...
ZOHO_ORG_ID=...
```

Install dependencies:

```powershell
npm install
pip install -r requirements.txt
```

Connection test:

```powershell
python test_connection.py
```

Run API locally:

```powershell
npx serverless offline
```

Base URL:

```text
http://localhost:3000/dev
```

## Curl Examples

Get jobs:

```bash
curl "http://localhost:3000/dev/jobs?page=1&limit=20"
```

Create candidate:

```bash
curl -X POST "http://localhost:3000/dev/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919999999999",
    "resume_url": "https://example.com/resume.pdf",
    "job_id": "YOUR_JOB_ID"
  }'
```

Get applications by job:

```bash
curl "http://localhost:3000/dev/applications?job_id=YOUR_JOB_ID&page=1&limit=20"
```

## Notes

- If Zoho field names differ in your account layout, adjust mappings in zoho_client.py.
- Errors from Zoho are returned as clean JSON with status code.
