import requests
import json
from typing import Dict, Any, Tuple, Optional

from .exceptions import APIError

def make_request(session: requests.Session, url: str, payload: Dict[str, Any], 
                timeout: int = 60, verify: bool = True):
    """
    Make an API request to the Terrakio API.
    
    Args:
        session: Requests session with authentication
        url: API endpoint URL
        payload: Request payload
        timeout: Request timeout in seconds
        verify: Verify SSL certificates
        
    Returns:
        Response object
        
    Raises:
        APIError: If the API returns an error
    """
    try:
        response = session.post(
            url,
            json=payload,
            timeout=timeout,
            verify=verify
        )
        
        # Handle HTTP errors
        if not response.ok:
            error_msg = f"API request failed: {response.status_code} {response.reason}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg += f" - {error_data['detail']}"
            except:
                pass
            
            raise APIError(error_msg)
        
        return response
            
    except requests.RequestException as e:
        raise APIError(f"Request failed: {str(e)}")