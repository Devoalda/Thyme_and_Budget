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

## Food

| Endpoint | Method | URL | Example Request |
| --- | --- | --- | --- |
| List all foods | GET | /food/ | |
| Create a new food | POST | /food/ | { "name": "Example Food", "expiry_date": "2022-12-31", "location": 1, "quantity": 10 } |
| Retrieve a food | GET | /food/{id}/ | |
| Update a food | PUT | /food/{id}/ | { "name": "Updated Food", "expiry_date": "2023-01-31", "location": 2, "quantity": 20 } |
| Partially update a food | PATCH | /food/{id}/ | { "name": "Partially Updated Food" } |
| Delete a food | DELETE | /food/{id}/ | |

## Location

| Endpoint | Method | URL | Example Request |
| --- | --- | --- | --- |
| List all locations | GET | /location/ | |
| Create a new location | POST | /location/ | { "username": "example_user", "location": "Example Location", "address": "123 Example St.", "postal_code": "12345" } |
| Retrieve a location | GET | /location/{id}/ | |
| Update a location | PUT | /location/{id}/ | { "username": "example_user", "location": "Updated Location", "address": "456 Updated St.", "postal_code": "67890" } |
| Partially update a location | PATCH | /location/{id}/ | { "location": "Partially Updated Location" } |
| Delete a location | DELETE | /location/{id}/ | |

## Collection

| Endpoint | Method | URL | Example Request |
| --- | --- | --- | --- |
| List all collections | GET | /collection/ | |
| Create a new collection | POST | /collection/ | { "phone_number": "1234567890", "food_item": 1, "quantity": 10 } |
| Retrieve a collection | GET | /collection/{id}/ | |
| Update a collection | PUT | /collection/{id}/ | { "phone_number": "0987654321", "food_item": 2, "quantity": 20 } |
| Partially update a collection | PATCH | /collection/{id}/ | { "quantity": 15 } |
| Delete a collection | DELETE | /collection/{id}/ | |

Please replace `{id}` with the actual ID of the item when making requests to the specific item endpoints.

## Swagger Documentation

You can also access the Swagger UI for a visual representation of the API and to test the endpoints at `http://127.0.0.1:8000/api/schema/swagger-ui/`.