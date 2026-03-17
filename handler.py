import json
import logging
from typing import Any, Dict

from zoho_client import ZohoClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _response(data: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Content-Type": "application/json",
        },
        "body": json.dumps(data),
    }


def _to_positive_int(raw_value: Any, default: int) -> int:
    try:
        value = int(raw_value)
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default


def get_jobs(event, context):
    query_params = event.get("queryStringParameters") or {}
    page = _to_positive_int(query_params.get("page", 1), 1)
    limit = _to_positive_int(query_params.get("limit", 50), 50)

    client = ZohoClient()
    data, status = client.get_jobs(page=page, limit=limit)
    return _response(data, status)


def create_candidate(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response({"error": "Invalid JSON body"}, 400)

    required = ["name", "email", "job_id"]
    missing = [field for field in required if not body.get(field)]
    if missing:
        return _response({"error": f"Missing required fields: {', '.join(missing)}"}, 400)

    client = ZohoClient()
    data, status = client.create_candidate(body)
    return _response(data, status)


def get_applications(event, context):
    query_params = event.get("queryStringParameters") or {}
    job_id = (query_params.get("job_id") or "").strip()
    if not job_id:
        return _response({"error": "job_id query parameter is required"}, 400)

    page = _to_positive_int(query_params.get("page", 1), 1)
    limit = _to_positive_int(query_params.get("limit", 50), 50)

    client = ZohoClient()
    data, status = client.get_applications(job_id=job_id, page=page, limit=limit)
    return _response(data, status)
