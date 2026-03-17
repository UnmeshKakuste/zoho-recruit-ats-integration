import os
import logging
from typing import Dict, Any, List, Optional, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ZohoClient:
    def __init__(self) -> None:
        self.client_id = os.environ.get("ZOHO_CLIENT_ID", "")
        self.client_secret = os.environ.get("ZOHO_CLIENT_SECRET", "")
        self.refresh_token = os.environ.get("ZOHO_REFRESH_TOKEN", "")
        self.recruit_base_url = os.environ.get("ZOHO_RECRUIT_BASE_URL", "https://recruit.zoho.in/recruit/v2").rstrip("/")
        self.accounts_base_url = os.environ.get("ZOHO_ACCOUNTS_BASE_URL", "https://accounts.zoho.in").rstrip("/")
        self.org_id = os.environ.get("ZOHO_ORG_ID", "")

        self._access_token: Optional[str] = None

    def _is_configured(self) -> bool:
        return all([self.client_id, self.client_secret, self.refresh_token])

    def _get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        if not self._is_configured():
            raise ValueError("Missing Zoho credentials in environment variables")

        token_url = f"{self.accounts_base_url}/oauth/v2/token"
        payload = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }

        response = requests.post(token_url, data=payload, timeout=15)
        if response.status_code != 200:
            raise RuntimeError(f"Zoho token refresh failed: {response.text}")

        token_data = response.json()
        self._access_token = token_data.get("access_token")
        if not self._access_token:
            raise RuntimeError("Zoho token endpoint returned no access_token")

        return self._access_token

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Zoho-oauthtoken {self._get_access_token()}",
            "Content-Type": "application/json",
        }
        if self.org_id:
            headers["X-ORG-ID"] = self.org_id
        return headers

    def _request(self, method: str, path: str, *, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.recruit_base_url}/{path.lstrip('/')}"
        return requests.request(method, url, headers=self._headers(), params=params, json=json_body, timeout=20)

    def _extract_zoho_data(self, response_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        return response_json.get("data", []) if isinstance(response_json, dict) else []

    def _pagination_meta(self, response_json: Dict[str, Any], page: int, limit: int, current_count: int) -> Dict[str, Any]:
        info = response_json.get("info", {}) if isinstance(response_json, dict) else {}
        more_records = bool(info.get("more_records", False))
        return {
            "page": page,
            "limit": limit,
            "count": current_count,
            "has_next": more_records,
        }

    def _map_job_status(self, value: Optional[str]) -> str:
        normalized = (value or "").strip().lower()
        if normalized in {"open", "active", "published"}:
            return "OPEN"
        if normalized in {"closed", "inactive", "filled"}:
            return "CLOSED"
        return "DRAFT"

    def _map_application_status(self, value: Optional[str]) -> str:
        normalized = (value or "").strip().lower()
        if normalized in {"applied", "new", "submitted"}:
            return "APPLIED"
        if normalized in {"screening", "review", "under review", "interview"}:
            return "SCREENING"
        if normalized in {"rejected", "disqualified"}:
            return "REJECTED"
        if normalized in {"hired", "offer accepted", "joined"}:
            return "HIRED"
        return "APPLIED"

    def _split_name(self, full_name: str) -> Tuple[str, str]:
        parts = [p for p in full_name.strip().split(" ") if p]
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], "Candidate"
        return parts[0], " ".join(parts[1:])

    def _handle_zoho_error(self, response: requests.Response) -> Tuple[Dict[str, Any], int]:
        try:
            payload = response.json()
        except ValueError:
            payload = {"message": response.text or "Unknown Zoho error"}

        return {
            "error": "ATS request failed",
            "status_code": response.status_code,
            "details": payload,
        }, response.status_code

    def get_jobs(self, page: int = 1, limit: int = 50) -> Tuple[Dict[str, Any], int]:
        try:
            response = self._request("GET", "/jobs", params={"page": page, "per_page": limit})
        except (ValueError, RuntimeError) as exc:
            return {"error": str(exc)}, 500
        except requests.RequestException as exc:
            return {"error": "Network error while fetching jobs", "details": str(exc)}, 503

        if response.status_code != 200:
            return self._handle_zoho_error(response)

        payload = response.json()
        items = self._extract_zoho_data(payload)

        jobs = []
        for item in items:
            location = item.get("city") or item.get("location") or item.get("country") or ""
            jobs.append(
                {
                    "id": str(item.get("id", "")),
                    "title": item.get("title") or item.get("name") or "",
                    "location": location,
                    "status": self._map_job_status(item.get("status")),
                    "external_url": item.get("url") or "",
                }
            )

        return {
            "data": jobs,
            "pagination": self._pagination_meta(payload, page, limit, len(jobs)),
        }, 200

    def create_candidate(self, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        full_name = payload.get("name", "").strip()
        first_name, last_name = self._split_name(full_name)

        candidate_payload = {
            "data": [
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": payload.get("email", ""),
                    "phone": payload.get("phone", ""),
                }
            ]
        }

        try:
            candidate_response = self._request("POST", "/candidates", json_body=candidate_payload)
        except (ValueError, RuntimeError) as exc:
            return {"error": str(exc)}, 500
        except requests.RequestException as exc:
            return {"error": "Network error while creating candidate", "details": str(exc)}, 503

        if candidate_response.status_code not in (200, 201):
            return self._handle_zoho_error(candidate_response)

        candidate_json = candidate_response.json()
        candidate_data = self._extract_zoho_data(candidate_json)
        candidate_id = ""
        if candidate_data:
            details = candidate_data[0].get("details", {})
            candidate_id = str(details.get("id", ""))

        if not candidate_id:
            return {
                "error": "Candidate creation succeeded but no candidate id returned",
                "details": candidate_json,
            }, 502

        application_payload = {
            "data": [
                {
                    "candidate_id": candidate_id,
                    "job_id": payload.get("job_id"),
                    "status": "Applied",
                }
            ]
        }

        try:
            app_response = self._request("POST", "/applications", json_body=application_payload)
        except requests.RequestException as exc:
            return {
                "error": "Candidate created, but network error while creating application",
                "candidate_id": candidate_id,
                "details": str(exc),
            }, 503

        if app_response.status_code not in (200, 201):
            error_payload, status = self._handle_zoho_error(app_response)
            return {
                "error": "Candidate created but failed to attach to job",
                "candidate_id": candidate_id,
                "application_error": error_payload,
            }, status

        app_json = app_response.json()
        app_data = self._extract_zoho_data(app_json)
        app_id = ""
        if app_data:
            app_details = app_data[0].get("details", {})
            app_id = str(app_details.get("id", ""))

        return {
            "id": candidate_id,
            "name": full_name,
            "email": payload.get("email"),
            "job_id": payload.get("job_id"),
            "application_id": app_id,
        }, 201

    def get_applications(self, job_id: str, page: int = 1, limit: int = 50) -> Tuple[Dict[str, Any], int]:
        try:
            response = self._request(
                "GET",
                "/applications",
                params={"job_id": job_id, "page": page, "per_page": limit},
            )
        except (ValueError, RuntimeError) as exc:
            return {"error": str(exc)}, 500
        except requests.RequestException as exc:
            return {"error": "Network error while fetching applications", "details": str(exc)}, 503

        if response.status_code == 204:
            return {
                "data": [],
                "pagination": {"page": page, "limit": limit, "count": 0, "has_next": False},
            }, 200

        if response.status_code != 200:
            return self._handle_zoho_error(response)

        payload = response.json()
        items = self._extract_zoho_data(payload)

        applications = []
        for item in items:
            candidate_lookup = item.get("candidate") or {}
            candidate_name = ""
            if isinstance(candidate_lookup, dict):
                candidate_name = candidate_lookup.get("name", "")
            status_val = item.get("status") or item.get("stage")

            applications.append(
                {
                    "id": str(item.get("id", "")),
                    "candidate_name": candidate_name,
                    "email": item.get("email") or "",
                    "status": self._map_application_status(status_val),
                }
            )

        return {
            "data": applications,
            "pagination": self._pagination_meta(payload, page, limit, len(applications)),
        }, 200
