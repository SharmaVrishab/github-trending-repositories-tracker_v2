"""
GitHub Authentication Script
Supports multiple authentication methods: Personal Access Token, OAuth, Device Flow, and GitHub App
"""

import os
import time
import webbrowser
from typing import Any, Dict, Optional

import requests


class GitHubAuth:
    """Handle GitHub API authentication"""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub authentication

        Args:
            token: GitHub token (can also be set via GITHUB_TOKEN env var)
            token_type: Type of token - "pat", "bearer", or "auto" (default)
                       "auto" detects based on token prefix
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        # self.token_type = self._detect_token_type(token_type)
        self.base_url = "https://api.github.com"
        self.headers = self._build_headers()

    # def _detect_token_type(self, token_type: str) -> str:
    #     """Detect token type based on prefix or user specification"""
    #     if token_type != "auto":
    #         return token_type

    #     if not self.token:
    #         return "pat"

    #     # Auto-detect based on token prefix
    #     if self.token.startswith(("ghp_", "github_pat_")):
    #         return "pat"  # Personal Access Token
    #     elif self.token.startswith(("gho_", "Iv")):
    #         return "bearer"  # OAuth/App token
    #     elif self.token.startswith("ghs_"):
    #         return "bearer"  # GitHub App installation token
    #     else:
    #         return "pat"  # Default to PAT

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-GitHub-Auth",
        }
        if self.token:
            # if self.token_type == "bearer":
            #     headers["Authorization"] = f"Bearer {self.token}"
            # else:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def verify_auth(self) -> Dict[str, Any]:
        """
        Verify authentication and get user info

        Returns:
            dict: User information if authenticated, error message otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/user", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            return {"authenticated": True, "user": response.json()}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {"authenticated": False, "error": "Invalid or missing token"}
            return {
                "authenticated": False,
                "error": f"HTTP Error: {e.response.status_code}",
            }
        except Exception as e:
            return {"authenticated": False, "error": str(e)}

    def get_user_repos(self, username: Optional[str] = None) -> list:
        """
        Get repositories for authenticated user or specified username

        Args:
            username: GitHub username (optional, defaults to authenticated user)

        Returns:
            list: List of repositories
        """
        if username:
            url = f"{self.base_url}/users/{username}/repos"
        else:
            url = f"{self.base_url}/user/repos"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            return []

    def create_repo(
        self, name: str, private: bool = False, description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new repository

        Args:
            name: Repository name
            private: Whether repo should be private
            description: Repository description

        Returns:
            dict: Repository data or error message
        """
        data = {"name": name, "private": private, "description": description}

        try:
            response = requests.post(
                f"{self.base_url}/user/repos",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


class GitHubDeviceFlow:
    """Handle GitHub Device Flow authentication (for CLI apps)"""

    def __init__(self, client_id: str):
        """
        Initialize Device Flow authentication

        Args:
            client_id: Your GitHub OAuth App client ID
        """
        self.client_id = client_id
        self.base_url = "https://github.com"

    def start_device_flow(self, scopes: str = "repo user") -> Dict[str, Any]:
        """
        Start the device flow authentication process

        Args:
            scopes: Space-separated list of scopes (e.g., "repo user")

        Returns:
            dict: Contains device_code, user_code, verification_uri, etc.
        """
        try:
            response = requests.post(
                f"{self.base_url}/login/device/code",
                data={"client_id": self.client_id, "scope": scopes},
                headers={"Accept": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def poll_for_token(self, device_code: str, interval: int = 5) -> Dict[str, Any]:
        """
        Poll GitHub to check if user has authorized the device

        Args:
            device_code: Device code from start_device_flow()
            interval: Seconds to wait between polls

        Returns:
            dict: Contains access_token if successful, or error
        """
        try:
            response = requests.post(
                f"{self.base_url}/login/oauth/access_token",
                data={
                    "client_id": self.client_id,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def authenticate(
        self, scopes: str = "repo user", open_browser: bool = True
    ) -> Optional[str]:
        """
        Complete device flow authentication process

        Args:
            scopes: Space-separated list of scopes
            open_browser: Whether to auto-open browser

        Returns:
            str: Access token if successful, None otherwise
        """
        # Step 1: Start device flow
        device_data = self.start_device_flow(scopes)

        if "error" in device_data:
            print(f"Error starting device flow: {device_data['error']}")
            return None

        user_code = device_data.get("user_code")
        verification_uri = device_data.get("verification_uri")
        device_code = device_data.get("device_code")
        interval = device_data.get("interval", 5)
        expires_in = device_data.get("expires_in", 900)

        # Step 2: Show user instructions
        print(f"\n{'=' * 50}")
        print(f"Please visit: {verification_uri}")
        print(f"And enter code: {user_code}")
        print(f"{'=' * 50}\n")

        if open_browser:
            try:
                webbrowser.open(verification_uri)
                print("Opening browser...")
            except:
                pass

        # Step 3: Poll for token
        print("Waiting for authorization...", end="", flush=True)
        start_time = time.time()

        while time.time() - start_time < expires_in:
            time.sleep(interval)

            result = self.poll_for_token(device_code, interval)

            if "access_token" in result:
                print("\n✓ Authorization successful!")
                return result["access_token"]

            elif result.get("error") == "authorization_pending":
                print(".", end="", flush=True)
                continue

            elif result.get("error") == "slow_down":
                interval += 5
                print(".", end="", flush=True)
                continue

            else:
                print(f"\n✗ Error: {result.get('error_description', 'Unknown error')}")
                return None

        print("\n✗ Authorization timed out")
        return None
