import json

from zoho_client import ZohoClient


def main() -> None:
    client = ZohoClient()
    data, status = client.get_jobs(page=1, limit=5)
    print(f"Status: {status}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
