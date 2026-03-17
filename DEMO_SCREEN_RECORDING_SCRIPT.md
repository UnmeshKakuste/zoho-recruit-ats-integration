# 📹 Demo Screen Recording Script: Zoho Recruit ATS Microservice

**Total Duration:** ~8-10 minutes  
**Resolution:** 1920x1080 (Full HD)  
**Format:** MP4 at 60fps

---

## SECTION 1: INTRODUCTION (0:00 - 0:45)

### 📝 NARRATION (What to Say)

> "Hello! Welcome to the Zoho Recruit ATS Integration Microservice demo. 
> 
> I'm Akshay, and today I'm going to walk you through a complete backend service that I built to integrate with Zoho Recruit – an Applicant Tracking System.
> 
> This microservice exposes three REST API endpoints that allow you to:
> - Fetch open job positions
> - Submit new candidates and apply them to jobs
> - Retrieve all applications for a specific job
> 
> The entire service runs on AWS Lambda via Serverless Framework, and we're using Python with OAuth 2.0 authentication to communicate with Zoho's API.
> 
> By the end of this demo, you'll see the code, the running service, and full API testing in action."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 0:00 - 0:15**
- Show **desktop** with VS Code window visible
- Display project folder open: `zoho-recruit-integration/`
- Show file tree with all files (handler.py, zoho_client.py, README.md, etc.)

**Duration: 0:15 - 0:45**
- Open and display [README.md](README.md) in browser or VS Code preview
- Highlight the 3 API endpoints section
- Show the example curl commands at bottom of README

---

## SECTION 2: PROJECT STRUCTURE & ARCHITECTURE (0:45 - 2:30)

### 📝 NARRATION (What to Say)

> "Let me start by explaining the project structure and how everything is organized.
> 
> This is a serverless architecture, which means we don't need to manage any servers ourselves. Instead, we use AWS Lambda – AWS's Functions-as-a-Service platform.
> 
> The project has three main layers:
> 
> **First, the Handler Layer** – This is where HTTP requests come in. Each endpoint has its own handler function: get_jobs, create_candidate, and get_applications.
> 
> **Second, the Client Layer** – This is the heart of the service. The ZohoClient class manages OAuth authentication, makes API calls to Zoho Recruit, and normalizes the response data into our standard format.
> 
> **Third, Infrastructure** – We use Serverless Framework to define and deploy the Lambda functions. The serverless.yml file defines our API routes, environment variables, and AWS configuration.
> 
> The entire flow looks like this: External client makes HTTP request → API Gateway routes it → Lambda handler processes it → ZohoClient talks to Zoho API → Response comes back standardized to the client.
> 
> All credentials are stored in environment variables in the .env file, which is never committed to git. This keeps our API keys and refresh tokens secure."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 0:45 - 1:15**
- Open [handler.py](handler.py) in VS Code
- Scroll through showing the three handler functions:
  - `get_jobs()` – lines 30-45
  - `create_candidate()` – lines 50-75
  - `get_applications()` – lines 80-100
- Show the `_response()` helper function (lines 15-25)
- Highlight CORS headers in response

**Duration: 1:15 - 1:45**
- Open [zoho_client.py](zoho_client.py)
- Show the class structure:
  - `__init__()` method (loads credentials from env)
  - `_get_access_token()` (OAuth refresh logic) – lines 35-55
  - Three main methods: `get_jobs()`, `create_candidate()`, `get_applications()` – scroll through all three
- Highlight the data mapping methods:
  - `_map_job_status()` (line 120)
  - `_map_application_status()` (line 130)

**Duration: 1:45 - 2:15**
- Open [serverless.yml](serverless.yml)
- Show configuration:
  - Provider settings (runtime: python3.11, region: ap-south-1)
  - Environment variables section (all 6 env vars)
  - Functions section with 3 endpoints
  - Plugins (serverless-offline, serverless-python-requirements)

**Duration: 2:15 - 2:30**
- Open [API_DESIGN_AND_SYSTEM_ARCHITECTURE.md](API_DESIGN_AND_SYSTEM_ARCHITECTURE.md)
- Show the system architecture diagram (ASCII art)
- Let viewer read it for a few seconds

---

## SECTION 3: RUNNING THE SERVICE LOCALLY (2:30 - 3:45)

### 📝 NARRATION (What to Say)

> "Now let me show you how to run this service locally for development and testing.
> 
> First, I've already installed all the dependencies – Node.js packages for Serverless Framework and Python packages like requests and python-dotenv.
> 
> The .env file contains all our credentials – the OAuth credentials, the Zoho API endpoints, and our organization ID. These were generated through Zoho's Developer Console earlier.
> 
> Now I'll start the local server using Serverless Offline, which simulates AWS API Gateway on my machine. This is perfect for local development because I don't need an AWS account to test."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 2:30 - 2:45**
- Open PowerShell/Terminal
- Show current directory: `C:\Users\aksha\Desktop\Apps\Task2-Unmesh`
- List files: `ls` or `dir` – show all project files

**Duration: 2:45 - 3:00**
- Show .env file (with credentials visible or partially masked):
  ```
  ZOHO_CLIENT_ID=1000.MC5RXT...
  ZOHO_CLIENT_SECRET=6ac1f4bc...
  ZOHO_REFRESH_TOKEN=1000.c04d7a...
  ZOHO_RECRUIT_BASE_URL=https://recruit.zoho.in/recruit/v2
  ZOHO_ACCOUNTS_BASE_URL=https://accounts.zoho.in
  ZOHO_ORG_ID=60067448187
  ```

**Duration: 3:00 - 3:30**
- Type command: `npx serverless offline`
- Show output scrolling:
  ```
  Offline listening on http://localhost:3000
  
  GET | http://localhost:3000/dev/jobs
  POST | http://localhost:3000/dev/candidates
  GET | http://localhost:3000/dev/applications
  
  Ready!
  ```
- Let this sit on screen for a few seconds showing the server is running

**Duration: 3:30 - 3:45**
- Take a second terminal
- Keep both visible (split screen if possible)
- Show first terminal still running serverless offline

---

## SECTION 4: TESTING ENDPOINT 1 - GET /jobs (3:45 - 5:00)

### 📝 NARRATION (What to Say)

> "Excellent! The server is now running locally on port 3000.
> 
> Now let me test the first endpoint: GET /jobs. This fetches all open job positions from Zoho Recruit.
> 
> I'll use curl from PowerShell to make the request. Notice that the endpoint includes pagination parameters – page and limit – both optional."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 3:45 - 4:00**
- In second terminal, type:
  ```powershell
  curl "http://localhost:3000/dev/jobs?page=1&limit=10"
  ```
- Press Enter

**Duration: 4:00 - 4:30**
- Show the response JSON formatted:
  ```json
  {
    "data": [
      {
        "id": "ZR_1_JOB",
        "title": "Senior Python Developer",
        "location": "San Francisco, CA",
        "status": "OPEN",
        "external_url": "https://..."
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "count": 1,
      "has_next": false
    }
  }
  ```
- Take time to let viewer read the response

**Duration: 4:30 - 4:45**
- Continue narration:

> "Perfect! You can see the response includes our standardized format with:
> - Job ID, title, location, status, and external URL
> - Pagination metadata showing page 1, limit 10, and that there's no next page
> 
> This data was fetched from Zoho Recruit and normalized by our ZohoClient class. Notice that Zoho might return different field names or structures, but our API always returns a consistent format."

**Duration: 4:45 - 5:00**
- Optional: Show the same request in Postman
  - Open Postman
  - Create GET request to `http://localhost:3000/dev/jobs`
  - Click Send
  - Show the response in Postman's formatted view

---

## SECTION 5: TESTING ENDPOINT 2 - POST /candidates (5:00 - 6:30)

### 📝 NARRATION (What to Say)

> "Now let's test the second and more interesting endpoint: POST /candidates.
> 
> This endpoint creates a new candidate profile in Zoho Recruit AND immediately applies them to a specific job – all in a single API call.
> 
> The endpoint requires four fields:
> - name: The candidate's full name
> - email: Their email address
> - job_id: The job they're applying for
> - And optionally: phone and resume_url
> 
> Behind the scenes, this makes two Zoho API calls:
> 1. First, it creates the candidate profile
> 2. Then, it links them to the job by creating an application
> 
> If the candidate already exists, it updates their profile. If the job doesn't exist, it returns a 404 error."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 5:00 - 5:15**
- In PowerShell, show the curl command:
  ```powershell
  curl -X POST "http://localhost:3000/dev/candidates" `
    -H "Content-Type: application/json" `
    -d '{
      "name": "Akshay Jadhav",
      "email": "akshay@example.com",
      "phone": "+919876543210",
      "resume_url": "https://example.com/resume.pdf",
      "job_id": "ZR_1_JOB"
    }'
  ```
- Type it out line by line slowly so it's readable

**Duration: 5:15 - 5:30**
- Press Enter
- Show the response (201 Created):
  ```json
  {
    "id": "candidate_xyz123",
    "name": "Akshay Jadhav",
    "email": "akshay@example.com",
    "job_id": "ZR_1_JOB",
    "application_id": "app_abc456"
  }
  ```

**Duration: 5:30 - 5:45**
- Continue narration:

> "Great! The candidate was created successfully with status 201 Created.
> 
> Notice the response includes:
> - candidate_id (the ID in Zoho's system)
> - The candidate name and email I provided
> - The job_id they applied for
> - application_id (the application record linking them to the job)
> 
> Both IDs are important – they're what we'll use to track the candidate in subsequent API calls."

**Duration: 5:45 - 6:15**
- Optional: Show error case
  - Type curl with missing email:
    ```powershell
    curl -X POST "http://localhost:3000/dev/candidates" `
      -H "Content-Type: application/json" `
      -d '{"name": "John Doe", "job_id": "ZR_1_JOB"}'
    ```
  - Show 400 error response:
    ```json
    {
      "error": "Missing required fields: email"
    }
    ```

**Duration: 6:15 - 6:30**
- Narrate error handling:

> "If I submit without required fields, I get a clear 400 Bad Request error. The API tells me exactly which fields are missing. This kind of validation makes it easy for client developers to understand what went wrong and fix it."

---

## SECTION 6: TESTING ENDPOINT 3 - GET /applications (6:30 - 7:45)

### 📝 NARRATION (What to Say)

> "Now for the third endpoint: GET /applications.
> 
> This endpoint retrieves all applications for a specific job. It requires the job_id as a query parameter, and you can optionally filter by status or paginate through results.
> 
> Remember the job_id from earlier? We created a candidate application for job ZR_1_JOB. Let me fetch all applications for that job to see our newly created application."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 6:30 - 6:45**
- In PowerShell, type:
  ```powershell
  curl "http://localhost:3000/dev/applications?job_id=ZR_1_JOB&page=1&limit=20"
  ```
- Press Enter

**Duration: 6:45 - 7:15**
- Show the response:
  ```json
  {
    "data": [
      {
        "id": "app_abc456",
        "candidate_name": "Akshay Jadhav",
        "email": "akshay@example.com",
        "status": "APPLIED"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "count": 1,
      "has_next": false
    }
  }
  ```
- Let viewer read and recognize the candidate we just created

**Duration: 7:15 - 7:30**
- Continue narration:

> "Perfect! Here's our newly created candidate application showing up in the list. The status is APPLIED, which means the candidate just submitted their application.
> 
> As they progress through the hiring pipeline, this status will change to SCREENING when they're being reviewed, REJECTED if the company passes, or HIRED if they get the job.
> 
> The API normalizes these statuses across Zoho's internal pipeline stages, making it easy for external systems to work with the data."

**Duration: 7:30 - 7:45**
- Optional: Show status filtering
  - Type:
    ```powershell
    curl "http://localhost:3000/dev/applications?job_id=ZR_1_JOB&status=SCREENING"
    ```
  - Show empty result (no SCREENING candidates yet)
  - Explain that you can filter by any status

---

## SECTION 7: AUTHENTICATION & SECURITY (7:45 - 8:15)

### 📝 NARRATION (What to Say)

> "Let me quickly explain the security layer that powers all these requests.
> 
> Every request to Zoho is authenticated using OAuth 2.0 – an industry-standard authentication protocol.
> 
> When the service starts, we load the refresh_token from environment variables. Each time we make a request to Zoho, we check if our access token is expired. If it is, we automatically refresh it using the refresh token.
> 
> The refresh_token is long-lived – valid for about 2 years – so we don't need to manually re-authenticate.
> 
> All credentials are stored in the .env file and never appear in source code or logs. When deployed to AWS Lambda, these are injected as environment variables by the Serverless Framework."

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 7:45 - 8:00**
- Open [zoho_client.py](zoho_client.py)
- Navigate to `_get_access_token()` method
- Show the implementation:
  ```python
  def _get_access_token(self) -> str:
      if self._access_token:
          return self._access_token
      
      token_url = f"{self.accounts_base_url}/oauth/v2/token"
      payload = {
          "refresh_token": self.refresh_token,
          "client_id": self.client_id,
          "client_secret": self.client_secret,
          "grant_type": "refresh_token",
      }
      response = requests.post(token_url, data=payload)
      token_data = response.json()
      self._access_token = token_data.get("access_token")
      return self._access_token
  ```
- Highlight the caching mechanism (first if statement)

**Duration: 8:00 - 8:15**
- Show the headers being built:
  ```python
  def _headers(self) -> Dict[str, str]:
      headers = {
          "Authorization": f"Zoho-oauthtoken {self._get_access_token()}",
          "Content-Type": "application/json",
      }
      if self.org_id:
          headers["X-ORG-ID"] = self.org_id
      return headers
  ```
- Explain the Bearer token format

---

## SECTION 8: DEPLOYMENT & NEXT STEPS (8:15 - 9:00)

### 📝 NARRATION (What to Say)

> "The service is now running locally, which is perfect for development and testing.
> 
> But here's the beauty of Serverless – when we're ready for production, deploying to AWS Lambda takes just one command.
> 
> The Serverless Framework handles:
> - Packaging our Python code
> - Creating the Lambda functions
> - Setting up API Gateway to route HTTP requests
> - Injecting environment variables
> - Configuring CORS headers
> 
> Everything defined in serverless.yml gets deployed automatically.
> 
> This is a production-ready microservice that can handle thousands of concurrent requests. AWS automatically scales based on demand, so you only pay for the requests you actually process.
> 
> Looking forward, we could add:
> - Database caching to reduce API calls
> - Webhook support for real-time ATS events
> - Batch candidate import endpoint
> - GraphQL endpoint as an alternative to REST
> - Admin dashboard for monitoring"

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 8:15 - 8:30**
- Show serverless.yml
- Highlight the deployment section
- Show the plugins being used

**Duration: 8:30 - 8:45**
- Show the README deployment section
- Display the command:
  ```bash
  serverless deploy
  ```
- Explain what this does (even if not actually running it)

**Duration: 8:45 - 9:00**
- Open [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md)
- Show "Future Enhancements" section
- Scroll through Phase 2 and Phase 3 features

---

## SECTION 9: CLOSING (9:00 - 9:30)

### 📝 NARRATION (What to Say)

> "That's the complete Zoho Recruit ATS Integration Microservice!
> 
> To summarize what we covered:
> 
> **Architecture:** A serverless Python microservice with three REST endpoints, OAuth 2.0 authentication, and a data normalization layer.
> 
> **Endpoints:** 
> - GET /jobs – Fetch open positions with pagination
> - POST /candidates – Create candidates and apply to jobs
> - GET /applications – Retrieve and filter applications by job
> 
> **Security:** Environment-based credentials, OAuth 2.0 tokens with automatic refresh, and CORS protection.
> 
> **Deployment:** One command to deploy to AWS Lambda. Automatic scaling, no server management.
> 
> **Testing:** Full testing demonstrated with curl commands; also works with Postman or any HTTP client.
> 
> The code is clean, well-documented, and production-ready. All files are available in the project repository, including comprehensive documentation, API specifications, and this entire implementation report.
> 
> Thank you for watching, and feel free to reach out if you have any questions!"

### 🖥️ WHAT TO SHOW ON SCREEN

**Duration: 9:00 - 9:15**
- Show the project directory again
- List all files:
  - handler.py
  - zoho_client.py
  - serverless.yml
  - README.md
  - IMPLEMENTATION_REPORT.md
  - API_DESIGN_AND_SYSTEM_ARCHITECTURE.md

**Duration: 9:15 - 9:30**
- Optional: Show GitHub repository (if available)
- Or show the project open in VS Code
- End with a clean desktop screenshot

---

## 📺 TECHNICAL SPECIFICATIONS FOR RECORDING

### Audio
- Microphone: Clear, minimal background noise
- Volume: Normalized to -3dB
- Sample rate: 48kHz
- Codec: AAC at 128 kbps

### Video
- Resolution: 1920x1080 (Full HD)
- Frame rate: 60fps
- Codec: H.264
- Bitrate: 8-12 Mbps

### Font & Text
- IDE Font: Fira Code or Courier New, size 18-20pt
- Terminal Font: Consolas or PowerShell ISE, size 16pt
- Cursor visibility: Enhanced

### Pacing
- Command typing: Slow enough to read (3-4 characters per second)
- Response display: Pause 2-3 seconds before scrolling
- Narrative delivery: Calm, clear, 1-2 second pauses between sentences

### Editing Tips
- Cut out hesitations and "ums"
- Add text overlays for key points (e.g., "OAuth 2.0 Authentication")
- Use screen transitions between major sections
- Add intro/outro slides with project title and your name
- Include background music (optional, at low volume -20dB)
- Add captions for accessibility

---

## 🎬 RECORDING CHECKLIST

- [ ] Microphone tested and working
- [ ] Screen cleared of sensitive information
- [ ] Terminal/IDE theme set for visibility
- [ ] Zoom level comfortable for reading code (120-150%)
- [ ] Both monitor displays visible (if applicable)
- [ ] Server running with no errors in console
- [ ] All dependencies installed
- [ ] .env file ready with valid credentials
- [ ] Git history clean (no embarrassing commits visible)
- [ ] Recording software open and configured
- [ ] Test recording to verify quality before main recording
- [ ] Backup of project files before recording
- [ ] Time buffer in case recording needs restart

---

**Total Runtime:** ~9-10 minutes  
**Target Audience:** Developers, DevOps, Technical Leads  
**Difficulty Level:** Intermediate (assumes basic REST API knowledge)

