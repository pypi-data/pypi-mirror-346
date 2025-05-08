# Coentice Integration

This project provides an API and a Python package for managing datasource templates, including list, add, update, and delete operations.

## API Service

Built with FastAPI, deployable to Azure App Service.

### Endpoints
- `GET /datasources`: List all datasource names.
- `GET /datasources/{name}/template`: Get the template for a specific datasource.
- `POST /datasources`: Add a new datasource (body: `{name: str, template: list}`).
- `PUT /datasources/{name}`: Update a datasource (body: `{template: list}`).
- `DELETE /datasources/{name}`: Delete a datasource.

### Running Locally
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload