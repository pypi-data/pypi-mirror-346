import requests
from typing import Dict, Any
from .exceptions import APIError

class UserManagement:
    def __init__(self, api_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key
        })

    def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve user info by user ID.
        """
        endpoint = f"{self.api_url}/admin/users/{user_id}"
        try:
            response = self.session.get(endpoint, timeout=self.timeout, verify=self.verify)
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """
        Retrieve user info by email.
        """
        endpoint = f"{self.api_url}/admin/users/email/{email}"
        try:
            response = self.session.get(endpoint, timeout=self.timeout, verify=self.verify)
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def edit_user(
        self,
        user_id: str,
        uid: str = None,
        email: str = None,
        role: str = None,
        apiKey: str = None,
        groups: list = None,
        quota: int = None
    ) -> Dict[str, Any]:
        """
        Edit user info. Only provided fields will be updated.
        user_id is required and will be included in the payload.
        """
        endpoint = f"{self.api_url}/admin/users"
        payload = {"uid": user_id}

        if uid is not None:
            payload["uid"] = uid
        if email is not None:
            payload["email"] = email
        if role is not None:
            payload["role"] = role
        if apiKey is not None:
            payload["apiKey"] = apiKey
        if groups is not None:
            payload["groups"] = groups
        if quota is not None:
            payload["quota"] = quota

        try:
            response = self.session.patch(
                endpoint,
                json=payload,
                timeout=self.timeout,
                verify=self.verify,
                headers={"Content-Type": "application/json"}
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def list_users(self, substring: str = None):
        """
        List users, optionally filtering by a substring.
        """
        endpoint = f"{self.api_url}/admin/users/list"
        print("the url is ", endpoint)
        params = {}
        if substring:
            params["substring"] = substring

        try:
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def reset_quota(self, email: str, quota: int = None) -> Dict[str, Any]:
        """
        Reset the quota for a user by email.
        :param email: The user's email (required, will be in the URL and payload)
        :param quota: The new quota value (optional)
        :return: API response as a dictionary
        """
        endpoint = f"{self.api_url}/admin/users/reset_quota/{email}"
        payload = {"email": email}
        if quota is not None:
            payload["quota"] = quota
        print("the endpoint is ", endpoint)
        try:
            response = self.session.patch(
                endpoint,
                json=payload,
                timeout=self.timeout,
                verify=self.verify,
                headers={"Content-Type": "application/json"}
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def delete_user(self, uid: str) -> dict:
        """
        Delete a user by UID.
        :param uid: The user's UID (required, will be in the URL)
        :return: API response as a dictionary
        """
        endpoint = f"{self.api_url}/admin/users/{uid}"
        try:
            response = self.session.delete(
                endpoint,
                timeout=self.timeout,
                verify=self.verify,
                headers={"x-api-key": self.api_key}
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")