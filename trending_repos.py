import os

import requests
from dotenv import load_dotenv

load_dotenv("config.env")

CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")


def request_device_code(client_id, scopes="repo"):
    """Request device code and user code from GitHub"""

    response = requests.post(
        "https://github.com/login/device/code",
        data={"client_id": client_id, "scope": scopes},
        headers={"Accept": "application/json"},
    ).json()

    if "error" in response:
        return {"error": "error"}

    return {
        "device_code": response["device_code"],
        "user_code": response["user_code"],
        "verification_uri": response["verification_uri"],
        "interval": response.get("interval", 5),
    }


if __name__ == "__main__":
    # Step 1: Request device
    print(type(CLIENT_ID))
    device_info = request_device_code(CLIENT_ID)
    if device_info:
        print(
            f"Go to {device_info['verification_uri']} and enter code: {device_info['user_code']}"
        )
    # # Step 2: Poll for access token
    # access_token = poll_for_access_token(
    #     CLIENT_ID, device_info["device_code"], device_info["interval"]
    # )

    # # Step 3: Fetch trending repos (last 7 days)
    # trending_repos = fetch_trending_repos(access_token, days=7, top_n=10)

    # # Step 4: Display results
    # print("\n🔥 Top trending repositories in the last 7 days:\n")
    # for repo in trending_repos:
    #     print(
    #         f"{repo['full_name']} - ⭐ {repo['stargazers_count']} - {repo['html_url']}"
    #     )
