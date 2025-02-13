# Backpack.tf Listings

## Overview 

**Backpack.tf Listings** is a FastAPI application designed for seamless interaction with [Backpack.tf](https://backpack.tf), a platform that provides real-time listings data for virtual items in Team Fortress 2. This project utilizes websocket connections to receive live updates from [Backpack.tf](https://backpack.tf) and employs its API to fetch and store listings data in a MongoDB database. Users can easily access this data through a RESTful API, making it a vital resource for traders and developers within the Team Fortress 2 community.

## Key Features

- **Real-time Data Updates**: Establishes websocket connections to receive live updates on item listings.
- **RESTful API**: Provides structured endpoints for retrieving and managing listings and user data.
- **High Performance**: Optimized to process over 10,000 listings per minute with minimal latency.
- **Secure API Access**: Supports optional authentication via authorization tokens.
- **Scalable & Dockerized**: Easily deploy the application using Docker and Docker Compose.

## Table of Contents

1. [Installation](#installation)
   - [Prerequisites](#prerequisites)  
   - [Clone the Repository](#clone-the-repository)
   - [Set Up Environment Variables](#set-up-environment-variables)
   - [Run with Docker](#run-with-docker)
2. [API Usage](#api-usage)
   - [Get Listings](#get-listings)
   - [Delete Listings](#delete-listings)
   - [Get User](#get-user)
3. [WebSocket Usage](#websocket-usage)
   - [WebSocket Endpoint](#websocket-endpoint)
   - [Data Format](#data-format)
4. [License](#license)

---

## Installation

### Prerequisites

Ensure you have the following installed:

- **Docker** and **Docker Compose**

### Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/dixon2004/backpack.tf-listings.git
cd backpack.tf-listings
```

### Set Up Environment Variables

1. Rename `template.env` to `.env` in the root directory.

2. Open `.env` and set the following environment variables:
    
    ```bash
    AUTH_TOKEN = "your_auth_token_here"
    BPTF_TOKEN = "your_backpacktf_token_here" # Multiple tokens can be separated by commas
    SAVE_USER_DATA = False
    STEAM_API_KEY = "your_steam_api_key_here"
    ```

    - `AUTH_TOKEN`: Optionally specify an authorization token for API access. If left empty, authentication is disabled, allowing unrestricted access.
    - `BPTF_TOKEN`: Your Backpack.tf API token, obtainable from [here](https://backpack.tf/connections).
    - `SAVE_USER_DATA`: Set to `True` to enable saving user data in the database (Default is False). 
    - `STEAM_API_KEY`: Your Steam API key, obtainable from [here](https://steamcommunity.com/dev/apikey).

### Run with Docker

1. **Build and Start the Service**:

    ```bash
    docker-compose up --build -d
    ```
    This will build the necessary Docker image and start the application as a background service on port 8000.

2. **Stopping the Service**:

    To stop and remove the running containers, execute:
    ```bash
    docker-compose down
    ```

3. **Restarting the Service**:

    If you need to restart the service after making changes to the environment variables or code:
    ```bash
    docker-compose down && docker-compose up --build -d
    ```

4. **Checking Logs**:

    To monitor the service logs in real-time:
    ```bash
    docker-compose logs -f
    ```

---

## API Usage

The **Backpack.tf Listings** application provides a RESTful API with the following endpoints:

### Get Listings

- **Endpoint**: `GET /listings`
- **Query Parameters**:
  - `sku`: The SKU of the item for which to fetch listings.
- **Authorization**: A valid authorization token is required if `AUTH_TOKEN` is set in the environment variables.
- **Response**: Returns listings data in JSON format.

**Example Request**:
```bash
curl -H "Authorization: YOUR_AUTH_TOKEN" "http://localhost:8000/listings?sku=YOUR_SKU"
```

### Delete Listings

- **Endpoint**: `DELETE /listings/{sku}`
- **Query Parameters**:
  - `sku`: The SKU of the item for which to delete all listings.
- **Authorization**: A valid authorization token is required if `AUTH_TOKEN` is set in the environment variables.
- **Response**: Returns a success message in JSON format.

**Example Request**:
```bash
curl -X DELETE -H "Authorization: YOUR_AUTH_TOKEN" "http://localhost:8000/listings/YOUR_SKU"
```

### Get User

- **Endpoint**: `GET /user`
- **Query Parameters**:
  - `steamid`: The Steam ID of the user to retrieve.
- **Authorization**: A valid authorization token is required if `AUTH_TOKEN` is set in the environment variables.
- **Response**: Returns user data in JSON format.

**Example Request**:
```bash
curl -H "Authorization: YOUR_AUTH_TOKEN" "http://localhost:8000/user?steamid=STEAM_ID"
```

## WebSocket Usage

The **Backpack.tf Listings** application supports a websocket connection that allows clients to receive real-time updates on item listings for Team Fortress 2.

### WebSocket Endpoint

- **Endpoint**: `ws://localhost:8000/ws`
- **Authorization**: No authorization token is required to connect to the websocket.

### Data Format

When updates are received via the websocket, the data is structured as follows:

```json
[
   {
       "sku": "item_sku",
       "name": "item_name"
   }
]
```

This format provides the SKU and name of the item that has been updated, enabling clients to react to market changes in real time.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.