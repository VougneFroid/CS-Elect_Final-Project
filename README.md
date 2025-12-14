# Spaceship Management REST API

A Flask REST API for managing a spaceship fleet database.

## Features

- Full CRUD operations for Pilots, Ships, Ship Classes, Weapon Classes, and Ship-Weapons
- Advanced search with multiple criteria
- JSON and XML response formats
- Input validation with error messages
- 79 test cases

## Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the API

```bash
python app.py
```

API runs at `http://localhost:5000`

## API Endpoints

### Pilots
- `GET /api/pilots` - Get all pilots or search
- `GET /api/pilots/<id>` - Get specific pilot
- `POST /api/pilots` - Create pilot
- `PUT /api/pilots/<id>` - Update pilot
- `DELETE /api/pilots/<id>` - Delete pilot

**Search:** `?name=value&rank=value&min_flight_years=5&min_mission_success=80`

### Ships
- `GET /api/ships` - Get all ships or search
- `GET /api/ships/<id>` - Get specific ship
- `POST /api/ships` - Create ship
- `PUT /api/ships/<id>` - Update ship
- `DELETE /api/ships/<id>` - Delete ship

**Search:** `?name=value&ship_class_id=1&pilot_id=2&min_capacity=100&max_speed=500`

### Ship Classes
- `GET /api/ship-classes` - Get all ship classes or search
- `GET /api/ship-classes/<id>` - Get specific class
- `POST /api/ship-classes` - Create class
- `PUT /api/ship-classes/<id>` - Update class
- `DELETE /api/ship-classes/<id>` - Delete class

**Search:** `?name=value&description=value`

### Weapon Classes
- `GET /api/weapon-classes` - Get all weapon classes or search
- `GET /api/weapon-classes/<id>` - Get specific weapon
- `POST /api/weapon-classes` - Create weapon
- `PUT /api/weapon-classes/<id>` - Update weapon
- `DELETE /api/weapon-classes/<id>` - Delete weapon

**Search:** `?class=value&min_damage=30&max_damage=100&min_range=500`

### Ship Weapons
- `POST /api/ship-weapons` - Assign weapon to ship
- `DELETE /api/ship-weapons/<ship_id>/<class_id>/<weapon_id>` - Remove assignment

## Response Formats

**JSON (default):**
```bash
GET /api/pilots/1
```

**XML:**
```bash
GET /api/pilots/1?format=xml
```

## Testing

Run all tests:
```bash
pytest tests/test_api.py -v
```

Run specific tests:
```bash
pytest tests/test_api.py::TestPilotCRUD -v
pytest tests/test_api.py -k search
```

## Project Structure

```
csfilnal/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── shiperd_final.sql     # Database dump
├── models/               # Database models
├── utils/                # Validators, formatters, error handlers
└── tests/                # Test suite
```

## Notes

- MySQL reserved keywords `rank` and `range` use backticks in queries
- All endpoints support JSON and XML formats via `?format=xml`
- Test database has 20 ships, 6 pilots, 5 ship classes, 5 weapon classes


## Development Notes

### MySQL Reserved Keywords

The following fields use MySQL reserved keywords and require backticks in queries:
- `rank` in pilot table
- `range` in weapon_class table


### Known Issues

- Pytest may show MySQL teardown errors (2006) - these are cosmetic and don't affect test results (solved)

