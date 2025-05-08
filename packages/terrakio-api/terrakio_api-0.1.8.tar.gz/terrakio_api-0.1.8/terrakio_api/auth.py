import requests
from typing import Optional, Dict, Any

class AuthClient:
    def __init__(self, base_url: str = "https://dev-au.terrak.io", 
                 verify: bool = True, timeout: int = 60):
        """
        Initialize the Authentication Client for Terrakio API.
        
        Args:
            base_url: Authentication API base URL
            verify: Verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.token = None
        self.api_key = None
    
    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user account.
        
        Args:
            email: User email address
            password: User password
        
        Returns:
            API response data
        """
        endpoint = f"{self.base_url}/users/signup"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = {
            "email": email,
            "password": password
        }
        
        response = requests.post(
            endpoint, 
            headers=headers,
            json=payload,
            verify=self.verify,
            timeout=self.timeout
        )
        
        if not response.ok:
            error_msg = f"Signup failed: {response.status_code} {response.reason}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg += f" - {error_data['detail']}"
            except:
                pass
            raise Exception(error_msg)
        
        return response.json()
    
    def login(self, email: str, password: str) -> str:
        """
        Log in and obtain authentication token.
        
        Args:
            email: User email address
            password: User password
        
        Returns:
            Authentication token
        """
        endpoint = f"{self.base_url}/users/login"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = {
            "email": email,
            "password": password
        }
        
        response = requests.post(
            endpoint, 
            headers=headers,
            json=payload,
            verify=self.verify,
            timeout=self.timeout
        )
        
        if not response.ok:
            error_msg = f"Login failed: {response.status_code} {response.reason}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg += f" - {error_data['detail']}"
            except:
                pass
            raise Exception(error_msg)
        
        result = response.json()
        self.token = result.get("token")
        
        # Update session with authorization header using Bearer prefix
        if self.token:
            self.session.headers.update({
                "Authorization": self.token
            })
        
        return self.token
    
    def refresh_api_key(self) -> str:
        """
        Generate or refresh API key.
        
        Returns:
            API key
        """
        if not self.token:
            raise Exception("Not authenticated. Call login() first.")
        
        endpoint = f"{self.base_url}/users/refresh_key"
        
        # Use session with updated headers from login
        response = self.session.post(
            endpoint,
            verify=self.verify,
            timeout=self.timeout
        )
        
        if not response.ok:
            error_msg = f"API key generation failed: {response.status_code} {response.reason}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg += f" - {error_data['detail']}"
            except:
                pass
            raise Exception(error_msg)
        
        result = response.json()
        self.api_key = result.get("apiKey")
        return self.api_key
    
    def view_api_key(self) -> str:
        """
        Retrieve current API key.
        
        Returns:
            API key
        """
        if not self.token:
            raise Exception("Not authenticated. Call login() first.")
        
        endpoint = f"{self.base_url}/users/key"
        print("the endpoint is ", endpoint)
        # Use session with updated headers from login
        response = self.session.get(
            endpoint,
            verify=self.verify,
            timeout=self.timeout
        )
        
        if not response.ok:
            error_msg = f"Failed to retrieve API key: {response.status_code} {response.reason}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg += f" - {error_data['detail']}"
            except:
                pass
            raise Exception(error_msg)
        
        result = response.json()
        print("the view response is ", result)
        self.api_key = result.get("apiKey")
        return self.api_key