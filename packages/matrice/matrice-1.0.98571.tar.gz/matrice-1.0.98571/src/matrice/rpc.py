"""Module for RPC client handling Matrice.ai backend API requests."""

import os
from datetime import datetime, timedelta, timezone
from importlib.metadata import version
import requests
from matrice.token_auth import (
    AuthToken,
    RefreshToken,
)


class RPC:
    """RPC class for handling backend API requests with token-based authentication."""

    def __init__(
        self,
        access_key,
        secret_key,
        project_id=None,
    ):
        """Initialize the RPC client with optional project ID."""
        self.project_id = project_id
        self.BASE_URL = f"https://{os.environ['ENV']}.backend.app.matrice.ai"
        self.access_key = access_key
        self.secret_key = secret_key
        self.Refresh_Token = RefreshToken(access_key, secret_key)
        self.AUTH_TOKEN = AuthToken(
            access_key,
            secret_key,
            self.Refresh_Token,
        )
        self.url_projectID = f"projectId={self.project_id}" if self.project_id else ""
        try:
            self.sdk_version = version("matrice")
        except Exception:
            self.sdk_version = "0.0.0"

    def send_request(
        self,
        method,
        path,
        headers={},
        payload={},
        files=None,
        data=None,
    ):
        """Send an HTTP request to the specified endpoint."""
        self.refresh_token()
        request_url = f"{self.BASE_URL}{path}"
        request_url = self.add_project_id(request_url)
        if not headers:
            headers = {}
        headers["sdk_version"] = self.sdk_version
        response = None
        response_data = None
        try:
            response = requests.request(
                method,
                request_url,
                auth=self.AUTH_TOKEN,
                headers=headers,
                json=payload,
                data=data,
                files=files,
            )
            response_data = response.json()
        except Exception as e:
            error_text = response.text if response else "No response"
            raise Exception(
                f"Error in sending request payload: {payload} to {request_url} with response: {error_text}, response_data: {response_data}, error: {e}"
            )
        return response_data

    def get(self, path, params={}):
        """Send a GET request to the specified endpoint."""
        return self.send_request("GET", path, payload=params)

    def post(
        self,
        path,
        headers={},
        payload={},
        files=None,
        data=None,
    ):
        """Send a POST request to the specified endpoint."""
        return self.send_request(
            "POST",
            path,
            headers=headers,
            payload=payload,
            files=files,
            data=data,
        )

    def put(self, path, headers={}, payload={}):
        """Send a PUT request to the specified endpoint."""
        return self.send_request(
            "PUT",
            path,
            headers=headers,
            payload=payload,
        )

    def delete(self, path, headers={}, payload={}):
        """Send a DELETE request to the specified endpoint."""
        return self.send_request(
            "DELETE",
            path,
            headers=headers,
            payload=payload,
        )

    def refresh_token(self):
        """Refresh the authentication token if expired."""
        time_difference = datetime.utcnow().replace(
            tzinfo=timezone.utc
        ) - self.AUTH_TOKEN.expiry_time.replace(tzinfo=timezone.utc)
        time_diff = time_difference - timedelta(0)
        if time_diff.total_seconds() >= 0:
            self.AUTH_TOKEN = AuthToken(
                self.access_key,
                self.secret_key,
                self.Refresh_Token,
            )
        return

    def add_project_id(self, url):
        """Add project ID to the URL if present and not already included."""
        if not self.url_projectID or "?projectId" in url or "&projectId" in url:
            return url
        if "?" in url:
            url = url + "&" + self.url_projectID
        else:
            url = url + "?" + self.url_projectID
        return url
