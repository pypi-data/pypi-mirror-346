import requests
from typing import List, Dict, Any

class APIClient:
    """Client to interact with the Coentice Integration API."""
    
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    def get_datasources(self) -> List[str]:
        """Retrieve the list of datasource names from the API."""
        try:
            response = requests.get(f"{self.api_url}/datasources")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve datasources: {str(e)}")

    def get_datasource_template(self, name: str) -> List[Dict[str, Any]]:
        """Retrieve the template for a specific datasource from the API."""
        try:
            response = requests.get(f"{self.api_url}/datasources/{name}/template")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve template for '{name}': {str(e)}")

    def add_datasource(self, name: str, template: List[Dict[str, Any]]) -> None:
        """Add a new datasource via the API."""
        try:
            response = requests.post(f"{self.api_url}/datasources", json={"name": name, "template": template})
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to add datasource '{name}': {str(e)}")

    def update_datasource(self, name: str, template: List[Dict[str, Any]]) -> None:
        """Update an existing datasource via the API."""
        try:
            response = requests.put(f"{self.api_url}/datasources/{name}", json={"template": template})
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to update datasource '{name}': {str(e)}")

    def delete_datasource(self, name: str) -> None:
        """Delete a datasource via the API."""
        try:
            response = requests.delete(f"{self.api_url}/datasources/{name}")
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to delete datasource '{name}': {str(e)}")