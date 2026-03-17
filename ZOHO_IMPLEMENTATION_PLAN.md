# 🎯 Implementation Plan: Zoho Recruit ATS Integration Microservice

## Project Overview

Build a Python-based serverless microservice that:
- Integrates with **Zoho Recruit** ATS API
- Exposes 3 standardized REST endpoints
- Runs on AWS Lambda via Serverless Framework
- Uses `serverless-offline` for local development

---

## Phase 1: Project Setup

### File Structure
```
zoho-recruit-integration/
├── handler.py              # Lambda entry points (3 endpoints)
├── zoho_client.py          # Core Zoho Recruit API wrapper
├── serverless.yml          # Serverless Framework config
├── requirements.txt        # Python dependencies
├── package.json            # npm dependencies
├── .env                    # Secrets (DO NOT commit)
├── .env.template           # Template for secrets
├── .gitignore              # Ignore node_modules, cache, .env
├── test_connection.py      # Connection verification script
└── README.md               # Complete setup guide
```

### Dependencies
```
requests               # HTTP client
python-dotenv          # Environment variable management
```

### npm Packages (serverless.yml)
```
serverless             # v3+
serverless-offline     # Local testing
serverless-python-requirements  # Python dependency bundling
```

---

## Phase 2: Zoho Recruit API Integration

### Key Endpoints to Map

| Microservice | Zoho Recruit Endpoint | Method | Purpose |
|---|---|---|---|
| `GET /jobs` | `/recruit/v2/jobs` | GET | List open positions |
| `POST /candidates` | `/recruit/v2/candidates` + `/recruit/v2/applications` | POST | Create candidate + create application |
| `GET /applications` | `/recruit/v2/applications?filter=job_id` | GET | List applications for a job |

### Authentication
- **Method:** OAuth 2.0 Bearer Token
- **Header Format:** `Authorization: Zoho-oauthtoken {access_token}`
- **Token Storage:** Environment variables
  - `ZOHO_REFRESH_TOKEN` (for token refresh)
  - `ZOHO_CLIENT_ID`
  - `ZOHO_CLIENT_SECRET`
  - `ZOHO_ORG_ID` (Organization ID, sometimes user ID)

---

## Phase 3: Data Mapping Layer

### Field Mappings

#### Jobs Endpoint
| Zoho Field | Microservice Field | Transformation |
|---|---|---|
| `id` | `id` | Direct |
| `title` | `title` | Direct |
| `locations[0]` | `location` | Extract first location string |
| `status` | `status` | Map: `open` → `OPEN`, `closed` → `CLOSED`, `draft` → `DRAFT` |
| `shareable_url` | `external_url` | Direct |

#### Candidates Endpoint
| Microservice Field | Zoho Field | Note |
|---|---|---|
| `name` | `firstName` + `lastName` | Combine if needed |
| `email` | `email` | Direct |
| `phone` | `phone` | Direct |
| `resume_url` | (attachment) | Upload separately |
| `job_id` | `Job_ID` | Link to job |

#### Applications Endpoint
| Zoho Field | Microservice Field | Transformation |
|---|---|---|
| `id` | `id` | Direct |
| `Candidate_Name` | `candidate_name` | Direct |
| `email` | `email` | Direct from candidate |
| `stage` | `status` | Map: `Applied` → `APPLIED`, `Under Review` → `SCREENING`, `Rejected` → `REJECTED`, `Hired` → `HIRED` |

---

## Phase 4: API Specification

### 1. GET /jobs
**Query Parameters:**
- `page` (optional, default=1)
- `limit` (optional, default=50)

**Response:**
```json
{
  "data": [
    {
      "id": "job_123",
      "title": "Senior Python Developer",
      "location": "San Francisco, CA",
      "status": "OPEN",
      "external_url": "https://zoho.com/recruit/jobs/..."
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 150,
    "has_next": true
  }
}
```

**Error Cases:**
- `400`: Invalid page number
- `401`: Invalid/expired Zoho token
- `503`: Zoho API unreachable

---

### 2. POST /candidates
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "job_id": "job_123",
  "resume_url": "https://example.com/resume.pdf"
}
```

**Response (201 Created):**
```json
{
  "id": "candidate_456",
  "name": "John Doe",
  "email": "john@example.com",
  "job_id": "job_123",
  "application_id": "app_789"
}
```

**Error Cases:**
- `400`: Missing required fields, invalid email
- `404`: Job ID not found in Zoho
- `409`: Candidate already applied to this job
- `503`: Zoho API error

---

### 3. GET /applications
**Query Parameters:**
- `job_id` (required)
- `page` (optional, default=1)
- `limit` (optional, default=50)
- `status` (optional filter: APPLIED, SCREENING, REJECTED, HIRED)

**Response:**
```json
{
  "data": [
    {
      "id": "app_789",
      "candidate_name": "John Doe",
      "email": "john@example.com",
      "status": "SCREENING"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 12,
    "has_next": false
  }
}
```

**Error Cases:**
- `400`: Missing job_id
- `404`: Job not found
- `503`: Zoho API error

---

## Phase 5: Implementation Details

### Core Classes & Methods

#### `zoho_client.py`

```python
class ZohoClient:
    def __init__(self):
        # Load credentials from env
        self.access_token = self._get_valid_token()
        self.org_id = os.environ.get("ZOHO_ORG_ID")
        self.base_url = "https://recruit.zoho.com/recruit/v2"
    
    # Private method for token refresh
    def _get_valid_token(self):
        # Check if token is expired, refresh if needed
        pass
    
    # Public methods
    def get_jobs(self, page=1, limit=50):
        # Fetch jobs, normalize, return (data, status_code)
        pass
    
    def create_candidate(self, payload):
        # Create candidate + application, return (data, status_code)
        pass
    
    def get_applications(self, job_id, page=1, limit=50, status_filter=None):
        # Fetch applications with filters, return (data, status_code)
        pass
    
    # Helper methods
    def _extract_location(self, job_data):
        # Parse location array, return string
        pass
    
    def _map_job_status(self, zoho_status):
        # Convert Zoho status to standard format
        pass
    
    def _map_app_status(self, zoho_stage):
        # Convert Zoho pipeline stage to standard format
        pass
    
    def _handle_error(self, response):
        # Parse Zoho error, return formatted error dict
        pass
```

#### `handler.py`

```python
def get_jobs(event, context):
    # Parse query params, call client, return formatted response
    pass

def create_candidate(event, context):
    # Parse request body, validate, call client, return 201/400
    pass

def get_applications(event, context):
    # Parse query params, validate job_id, call client, return response
    pass

def _response(data, status_code=200):
    # Build Lambda HTTP response with CORS headers
    pass
```

---

## Phase 6: Configuration Files

### serverless.yml
```yaml
service: zoho-recruit-integration
useDotenv: true

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  stage: dev
  environment:
    ZOHO_CLIENT_ID: ${env:ZOHO_CLIENT_ID}
    ZOHO_CLIENT_SECRET: ${env:ZOHO_CLIENT_SECRET}
    ZOHO_REFRESH_TOKEN: ${env:ZOHO_REFRESH_TOKEN}
    ZOHO_ORG_ID: ${env:ZOHO_ORG_ID}

functions:
  getJobs:
    handler: handler.get_jobs
    events:
      - http:
          path: jobs
          method: get
          cors: true
  
  createCandidate:
    handler: handler.create_candidate
    events:
      - http:
          path: candidates
          method: post
          cors: true
  
  getApplications:
    handler: handler.get_applications
    events:
      - http:
          path: applications
          method: get
          cors: true

plugins:
  - serverless-offline
  - serverless-python-requirements

custom:
  serverless-offline:
    httpPort: 3000
  pythonRequirements:
    dockerizePip: non-linux
```

### .env.template
```env
ZOHO_CLIENT_ID=your_client_id_here
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REFRESH_TOKEN=your_refresh_token_here
ZOHO_ORG_ID=your_organization_id_here
```

---

## Phase 7: Testing Strategy

### 1. Connection Test (`test_connection.py`)
- Verify credentials are valid
- Test token refresh mechanism
- Confirm Zoho API is reachable

### 2. Unit Tests
- Mock Zoho API responses
- Test data normalization
- Test error handling

### 3. Integration Tests (Local)
```bash
npm run dev  # Start serverless-offline
# Run curl tests
curl http://localhost:3000/dev/jobs
curl -X POST http://localhost:3000/dev/candidates -d {...}
curl http://localhost:3000/dev/applications?job_id=xyz
```

### 4. Test Cases
| Endpoint | Method | Scenario | Expected |
|---|---|---|---|
| `/jobs` | GET | Valid request | 200 + job list |
| `/jobs` | GET | page=2 | 200 + page 2 data |
| `/candidates` | POST | Valid payload | 201 + app_id |
| `/candidates` | POST | Missing job_id | 400 + error |
| `/candidates` | POST | Duplicate application | 409 + error |
| `/applications` | GET | Valid job_id | 200 + app list |
| `/applications` | GET | Missing job_id | 400 + error |

---

## Phase 8: Documentation

### README.md Sections
1. **Setup Zoho Recruit Account**
   - Create free trial
   - Generate OAuth credentials
   - Find Organization ID
   - Create test job posting

2. **Installation Steps**
   - Clone repo
   - `npm install`
   - `pip install -r requirements.txt`
   - Copy `.env.template` → `.env`
   - Fill in credentials

3. **Running Locally**
   - `npx serverless offline`
   - Server runs at `http://localhost:3000/dev`

4. **API Examples**
   - curl commands for each endpoint
   - Expected responses
   - Error scenarios

5. **Deployment to AWS**
   - `serverless deploy`
   - CloudWatch monitoring
   - Lambda environment setup

---

## Phase 9: Error Handling & Edge Cases

### Network Errors
- Handle timeouts (default 10s)
- Retry logic for 5xx errors (backoff)
- Return 503 with meaningful message

### Data Validation
- Email format validation (regex or pydantic)
- Phone number format check
- Resume URL must be HTTPS
- Job ID must exist in Zoho

### Rate Limiting
- Track API calls per minute
- Return 429 if exceeded
- Suggest retry-after header

### Missing Credentials
- Check all required env vars on startup
- Log warnings during initialization
- Return 500 if critical env var missing

---

## Phase 10: Production Checklist

- [ ] Unit tests written & passing
- [ ] Input validation with pydantic
- [ ] Structured logging (JSON format)
- [ ] Error responses standardized
- [ ] Pagination metadata included
- [ ] CORS headers configured correctly
- [ ] Request ID tracking added
- [ ] README completed with all sections
- [ ] Test screenshots captured
- [ ] Deploy to AWS Lambda
- [ ] CloudWatch alarms configured
- [ ] API documentation in Swagger/OpenAPI format

---

## Getting Zoho Recruit Credentials

### Step 1: Create Zoho Account
Go to [zoho.com/recruit](https://www.zoho.com/recruit/)

### Step 2: Generate OAuth Credentials
1. Go to **Zoho Developer Console**
2. Create a new Application (Server-based)
3. Get:
   - `ZOHO_CLIENT_ID`
   - `ZOHO_CLIENT_SECRET`
   - `ZOHO_REFRESH_TOKEN` (via OAuth flow)

### Step 3: Find Organization ID
In Zoho Recruit dashboard → **Settings** → **Organization** → Copy **Organization ID**

### Step 4: Create Test Job
Create at least one job posting to test against

---

## Timeline Estimate
- Phase 1-2: 30 mins (setup + auth)
- Phase 3-4: 1 hr (API design + mapping)
- Phase 5-6: 1.5 hrs (core implementation)
- Phase 7: 1 hr (testing)
- Phase 8: 30 mins (documentation)
- **Total: ~5 hours**

---

## Ready? Provide:
1. Zoho Recruit API documentation link or spec file
2. Sample API responses (jobs, candidates, applications)
3. Your Zoho credentials (or I'll wait for you to generate them)

I'll then implement all 3 endpoints + handler + client in full!
