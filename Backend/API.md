# API Documentation

This document provides detailed descriptions of the API endpoints provided by the backend.

## Authentication

| Endpoint | Method | URL | Example Request |
| --- | --- | --- | --- |
| Register | POST | /account/register | { "username": "example_user", "password": "example_password" } |
| Login | POST | /api/token/ | { "username": "example_user", "password": "example_password" } |
| Refresh Token | POST | /api/token/refresh/ | { "refresh": "example_refresh_token" } |
| Logout (GET) | GET | /account/logout | |
| Logout (POST) | POST | /account/logout | |

## Recipes

| Endpoint | Method | URL | Example Request                                                             |
| --- | --- | --- |-----------------------------------------------------------------------------|
| List all recipes | GET | /recipe/ |                                                                             |
| Create a new recipe | POST | /recipe/ | { "title": "Example Recipe", "Instructions": "This is an example recipe." } |
| Retrieve a recipe | GET | /recipe/{id}/ |                                                                             |
| Update a recipe | PUT | /recipe/{id}/ | { "title": "Updated Recipe", "instructions": "This is an updated recipe." } |
| Partially update a recipe | PATCH | /recipe/{id}/ | { "title": "Partially Updated Recipe" }                                     |
| Delete a recipe | DELETE | /recipe/{id}/ |                                                                             |

Please replace `{id}` with the actual ID of the recipe when making requests to the specific recipe endpoints.

## Swagger Documentation

You can also access the Swagger UI for a visual representation of the API and to test the endpoints at `http://127.0.0.1:8000/api/schema/swagger-ui/`.