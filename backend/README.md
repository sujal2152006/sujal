# Museum Backend API (Flask + MongoDB)

## Setup
1. `pip install -r requirements.txt`
2. MongoDB running on localhost:27017
3. Update .env (API_KEY, MONGODB_URI, CLERK_SECRET_KEY)
4. `python app.py`

## API Key
Use `X-API-Key: your_secret_api_key_here_change_this` header.

## Endpoints
- POST /api/login - {email, password}
- GET/POST /api/tickets - tickets CRUD

Frontend fetch: `fetch('/api/tickets', {headers: {'X-API-Key': 'your_key'}})`
