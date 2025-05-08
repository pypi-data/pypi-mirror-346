from typing import List, Dict, Any
from copy import deepcopy

class DatasourceManager:
    """Manages datasource templates with list, add, update, and delete operations."""
    
    _templates = {
        "MSSQL": [
            {"name": "server_name", "type": "string", "encrypted": False},
            {"name": "database_name", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "MySQL": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "database", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "Tally": [
            {"name": "url", "type": "string", "encrypted": False},
            {"name": "company", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "QuickBooks": [
            {"name": "access_token", "type": "string", "encrypted": True},
            {"name": "refresh_token", "type": "string", "encrypted": True},
            {"name": "realm_id", "type": "string", "encrypted": False}
        ],
        "SharePoint": [
            {"name": "site_url", "type": "string", "encrypted": False},
            {"name": "client_id", "type": "string", "encrypted": True},
            {"name": "client_secret", "type": "string", "encrypted": True}
        ],
        "PostgreSQL": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "database", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "Oracle": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "service_name", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "MongoDB": [
            {"name": "connection_string", "type": "string", "encrypted": True}
        ],
        "Cassandra": [
            {"name": "contact_points", "type": "list", "encrypted": False},
            {"name": "keyspace", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "Redis": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "Amazon S3": [
            {"name": "access_key_id", "type": "string", "encrypted": True},
            {"name": "secret_access_key", "type": "string", "encrypted": True},
            {"name": "region", "type": "string", "encrypted": False}
        ],
        "Google BigQuery": [
            {"name": "project_id", "type": "string", "encrypted": False},
            {"name": "dataset_id", "type": "string", "encrypted": False},
            {"name": "credentials", "type": "string", "encrypted": True}
        ],
        "Salesforce": [
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True},
            {"name": "security_token", "type": "string", "encrypted": True}
        ],
        "SAP HANA": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "database", "type": "string", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ],
        "Elasticsearch": [
            {"name": "host", "type": "string", "encrypted": False},
            {"name": "port", "type": "int", "encrypted": False},
            {"name": "username", "type": "string", "encrypted": True},
            {"name": "password", "type": "string", "encrypted": True}
        ]
    }

    def get_datasources(self) -> List[str]:
        """Return the list of available datasource names."""
        return list(self._templates.keys())

    def get_datasource_template(self, name: str) -> List[Dict[str, Any]]:
        """Return the property template for a specific datasource."""
        template = self._templates.get(name)
        if not template:
            raise ValueError(f"Datasource '{name}' not found")
        return deepcopy(template)

    def add_datasource(self, name: str, template: List[Dict[str, Any]]) -> None:
        """Add a new datasource with its template."""
        if name in self._templates:
            raise ValueError(f"Datasource '{name}' already exists")
        self.validate_template(template)
        self._templates[name] = deepcopy(template)

    def update_datasource(self, name: str, template: List[Dict[str, Any]]) -> None:
        """Update an existing datasource's template."""
        if name not in self._templates:
            raise ValueError(f"Datasource '{name}' not found")
        self.validate_template(template)
        self._templates[name] = deepcopy(template)

    def delete_datasource(self, name: str) -> None:
        """Delete a datasource."""
        if name not in self._templates:
            raise ValueError(f"Datasource '{name}' not found")
        del self._templates[name]

    @staticmethod
    def validate_template(template: List[Dict[str, Any]]) -> None:
        """Validate the structure of a datasource template."""
        for prop in template:
            if not isinstance(prop, dict):
                raise ValueError("Each property must be a dictionary")
            if not all(key in prop for key in ["name", "type", "encrypted"]):
                raise ValueError("Each property must have 'name', 'type', and 'encrypted' keys")
            if not isinstance(prop["name"], str):
                raise ValueError("Property 'name' must be a string")
            if prop["type"] not in ["string", "int", "list"]:
                raise ValueError("Property 'type' must be 'string', 'int', or 'list'")
            if not isinstance(prop["encrypted"], bool):
                raise ValueError("Property 'encrypted' must be a boolean")

# Singleton instance
datasource_manager = DatasourceManager()