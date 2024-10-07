# Backpack.tf Listings

## Overview 

**Backpack.tf Listings** is a FastAPI application designed for seamless interaction with [Backpack.tf](https://backpack.tf), a platform that provides real-time listings data for virtual items in Team Fortress 2. This project utilizes websocket connections to receive live updates from [Backpack.tf](https://backpack.tf) and employs its API to fetch and store listings data in a MongoDB database. Users can easily access this data through a RESTful API, making it a vital resource for traders and developers within the Team Fortress 2 community.

## Key Features

- **Real-time Data Updates**: Establishes websocket connections to receive live updates on item listings in Team Fortress 2.
- **RESTful API**: Offers well-defined endpoints for fetching and managing listings and user data.
- **High Performance**: Capable of processing over 10,000 listings in under a minute, ensuring efficient data handling.
- **User Authentication**: Supports optional authorization tokens for secure API access.

## Table of Contents

1. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
   - [Set Up a Virtual Environment](#set-up-a-virtual-environment)
   - [Install Dependencies](#install-dependencies)
   - [Environment Variables](#environment-variables)
   - [Configuration](#configuration)
   - [Run the Application](#run-the-application)
   - [Optional: PM2 Setup for Linux Users](#optional-pm2-setup-for-linux-users)
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

- **Python 3.8** or higher.

### Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/dixon2004/backpack.tf-listings.git
cd backpack.tf-listings
```

### Set Up a Virtual Environment

Create and activate a virtual environment to manage dependencies:

- **Linux/macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

### Install Dependencies

Install the necessary Python packages using:

```bash
pip install -r requirements.txt
```

### Environment Variables

Set the following environment variables before running the application:

- `DATABASE_URL`: MongoDB connection string (e.g., `mongodb://localhost:27017`).
- `BPTF_TOKEN`: Your Backpack.tf API token, obtainable from [here](https://backpack.tf/connections).
- `STEAM_API_KEY`: Your Steam API key, obtainable from [here](https://steamcommunity.com/dev/apikey).

### Configuration

Customize the application settings via the `options.json` file located in the project directory. Here is the default configuration:

```json
{
    "save_user_data": false,
    "auth_token": "",  // Optionally provide an Auth Token. If left empty, no token is required for API access.
    "port": 8000
}
```

- `save_user_data`: Set to `true` to enable saving user data in the database.
- `auth_token`: Optionally specify an authorization token for API access. If left empty, no token will be required.
- `port`: Define the port number for the API (default is 8000).

### Run the Application

Start the application by executing:

```bash
python src/main.py
```

### Optional: PM2 Setup for Linux Users

**PM2** is a process manager that simplifies application management, including automatic restarts and log handling.

#### Install PM2

Install PM2 globally via npm:

```bash
npm install pm2 -g
```

#### Start the Application with PM2

Run the application as a background service using PM2:

```bash
pm2 start src/main.py --name backpack-tf-listings --interpreter python3
```

#### Configure Log Rotation

For details on setting up log rotation with PM2, refer to the [PM2 Logrotate Documentation](https://github.com/keymetrics/pm2-logrotate).

#### Enable PM2 on System Startup

Ensure PM2 restarts automatically on boot:

```bash
pm2 startup
pm2 save
```

#### Monitor the Application

Monitor the application’s status and logs with:

```bash
pm2 status
pm2 logs
```

---

## API Usage

The **Backpack.tf Listings** application provides a RESTful API with the following endpoints:

### Get Listings

- **Endpoint**: `GET /listings`
- **Query Parameters**:
  - `sku`: The SKU of the item for which to fetch listings.
- **Authorization**: A valid authorization token is required if specified in the `options.json` file.
- **Response**: Returns listings data in JSON format.

**Example Request**:
```bash
curl -H "Authorization: YOUR_AUTH_TOKEN" "http://localhost:8000/listings?sku=YOUR_SKU"
```

### Delete Listings

- **Endpoint**: `DELETE /listings/{sku}`
- **Query Parameters**:
  - `sku`: The SKU of the item for which to delete all listings.
- **Authorization**: A valid authorization token is required if specified in the `options.json` file.
- **Response**: Returns a success message in JSON format.

**Example Request**:
```bash
curl -X DELETE -H "Authorization: YOUR_AUTH_TOKEN" "http://localhost:8000/listings/YOUR_SKU"
```

### Get User

- **Endpoint**: `GET /user`
- **Query Parameters**:
  - `steamid`: The Steam ID of the user to retrieve.
- **Authorization**: A valid authorization token is required if specified in the `options.json` file.
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
