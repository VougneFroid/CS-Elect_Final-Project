# ShipERD - Spaceship Management API

A RESTful API for managing spaceships, pilots, ship classes, weapon classes, and ship weapon assignments. Built with Flask and MySQL, featuring JWT authentication for secure operations.

## Features

- **CRUD Operations** for pilots, ships, ship classes, weapon classes, and ship weapons
- **JWT Authentication** for secure API access
- **Advanced Search** capabilities with multiple filter criteria
- **RESTful Design** with proper HTTP methods and status codes
- **MySQL Database** with relational data integrity
- **Input Validation** for all data operations
- **Password Hashing** using secure algorithms
- **Token-based Authentication** with 24-hour expiration

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Authentication:** JWT (JSON Web Tokens)
- **Password Security:** Werkzeug password hashing
- **Testing:** pytest, requests library

## Prerequisites

Before running this project, make sure you have:

- Python 3.8 or higher
- MySQL server (XAMPP recommended for Windows)
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cs-elect.git
cd cs-elect
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Make sure MySQL is running (start XAMPP if using), then import the database schema:

```bash
mysql -u root -p < shiperd_final.sql
```

Or run the migration script:

```bash
python run_migration.py
```

### 5. Configure Environment (Optional)

Copy the example environment file and update with your settings:

```bash
copy .env.example .env
```

Edit `.env` to set your JWT secret key and database credentials.

### 6. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Base URL

```
http://localhost:5000/api
```

### Authentication

Most write operations (POST, PUT, DELETE) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### Register a New User

**POST** `/api/auth/register`

Request Body:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

Response (201):
```json
{
  "status": "success",
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Login

**POST** `/api/auth/login`

Request Body:
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

Response (200):
```json
{
  "status": "success",
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Pilot Endpoints

#### Get All Pilots

**GET** `/api/pilots`

Optional Query Parameters:
- `name` - Filter by name (partial match)
- `rank` - Filter by rank
- `min_flight_years` - Minimum flight years
- `min_mission_success` - Minimum mission success rate

Example: `/api/pilots?rank=Captain&min_mission_success=90`

#### Get Pilot by ID

**GET** `/api/pilots/<id>`

#### Create Pilot (Requires Auth)

**POST** `/api/pilots`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "name": "Han Solo",
  "flight_years": 15,
  "rank": "Captain",
  "mission_success": 95
}
```

#### Update Pilot (Requires Auth)

**PUT** `/api/pilots/<id>`

Headers: `Authorization: Bearer <token>`

Request Body:
```json
{
  "rank": "General",
  "mission_success": 98
}
```

#### Delete Pilot (Requires Auth)

**DELETE** `/api/pilots/<id>`

Headers: `Authorization: Bearer <token>`

### Ship Endpoints

#### Get All Ships

**GET** `/api/ships`

Optional Query Parameters:
- `name` - Filter by name
- `ship_class_id` - Filter by ship class
- `pilot_id` - Filter by pilot
- `min_capacity`, `max_capacity` - Capacity range
- `min_speed`, `max_speed` - Speed range
- `min_shield`, `max_shield` - Shield range

#### Get Ship by ID

**GET** `/api/ships/<id>`

#### Create Ship (Requires Auth)

**POST** `/api/ships`

Request Body:
```json
{
  "name": "Millennium Falcon",
  "capacity": 100,
  "speed": 150,
  "shield": 200,
  "ship_class_id": 1,
  "pilot_id": 1
}
```

#### Update Ship (Requires Auth)

**PUT** `/api/ships/<id>`

#### Delete Ship (Requires Auth)

**DELETE** `/api/ships/<id>`

### Ship Class Endpoints

#### Get All Ship Classes

**GET** `/api/ship-classes`

#### Create Ship Class (Requires Auth)

**POST** `/api/ship-classes`

Request Body:
```json
{
  "name": "Corvette",
  "description": "Fast and agile light capital ship"
}
```

#### Update/Delete Ship Class (Requires Auth)

**PUT/DELETE** `/api/ship-classes/<id>`

### Weapon Class Endpoints

#### Get All Weapon Classes

**GET** `/api/weapon-classes`

#### Create Weapon Class (Requires Auth)

**POST** `/api/weapon-classes`

Request Body:
```json
{
  "class": "Laser Cannon",
  "damage": 50,
  "reload_speed": 2,
  "spread": 10,
  "range": 1000
}
```

### Ship Weapons Endpoints

#### Get All Ship Weapons

**GET** `/api/ship-weapons`

#### Get Weapons for a Ship

**GET** `/api/ship-weapons/ship/<ship_id>`

#### Assign Weapon to Ship (Requires Auth)

**POST** `/api/ship-weapons`

Request Body:
```json
{
  "ship_id": 1,
  "ship_class_id": 1,
  "weapon_class_id": 1,
  "name": "Forward Laser"
}
```

## Usage Examples

### PowerShell

```powershell
# Register and get token
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" `
  -Method POST -ContentType "application/json" `
  -Body '{"username": "pilot1", "email": "pilot1@example.com", "password": "pass123"}'
$token = $response.token

# Create a pilot
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:5000/api/pilots" `
  -Method POST -ContentType "application/json" -Headers $headers `
  -Body '{"name": "Luke Skywalker", "flight_years": 10, "rank": "Commander", "mission_success": 98}'

# Get all pilots
Invoke-RestMethod -Uri "http://localhost:5000/api/pilots"
```

### Python (using requests)

```python
import requests

# Register
response = requests.post('http://localhost:5000/api/auth/register', json={
    'username': 'pilot1',
    'email': 'pilot1@example.com',
    'password': 'pass123'
})
token = response.json()['token']

# Create pilot
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:5000/api/pilots',
    headers=headers,
    json={
        'name': 'Luke Skywalker',
        'flight_years': 10,
        'rank': 'Commander',
        'mission_success': 98
    })

# Get all pilots
response = requests.get('http://localhost:5000/api/pilots')
pilots = response.json()
```

### Using Postman

1. Create a POST request to `/api/auth/register` or `/api/auth/login`
2. Copy the token from the response
3. For protected endpoints:
   - Go to Authorization tab
   - Select "Bearer Token"
   - Paste your token
4. Make your request

## Testing

### Automated Testing

Run the authentication test suite:

```bash
pip install requests
python test_auth.py
```




## Security Features

- **Password Hashing:** All passwords are hashed using Werkzeug's secure scrypt algorithm
- **JWT Tokens:** Signed tokens with 24-hour expiration
- **Protected Routes:** Write operations require valid authentication
- **Input Validation:** All inputs are validated before processing
- **SQL Injection Protection:** Parameterized queries prevent SQL injection

## Error Handling

The API returns standardized error responses:

```json
{
  "status": "error",
  "message": "Error description here"
}
```

Common HTTP status codes:
- `200 OK` - Successful GET/PUT/DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource
- `500 Internal Server Error` - Server error

## Database Schema

The database consists of 6 main tables:
- **users** - User accounts for authentication
- **pilots** - Pilot information
- **ships** - Ship details
- **ship_classes** - Ship class definitions
- **weapon_classes** - Weapon specifications
- **ship_weapons** - Ship-weapon assignments

See `shiperd_final.sql` for complete schema details.

## Author

Vougne Froid Alis BSCS3B2 - CS-Elect Final Project


