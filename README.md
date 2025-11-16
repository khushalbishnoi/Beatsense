# Beatsense — Minimal End-to-end Demo

This repository is a small demo showing a React frontend and Flask backend integrated with Spotify to produce audio-feature based recommendations.

## Run with Docker (recommended)

1. Copy env file and add Spotify credentials:
```bash
cp .env.example .env
# Edit .env and fill SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
```

2. Build and start:
```bash
docker-compose build
docker-compose up --remove-orphans
```

- Frontend: http://localhost:3000  
- Backend: http://localhost:5000  
- Health: http://localhost:5000/health

## Development (without Docker)

### Backend
```bash
cd MLmodelandBackend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
python app.py
```

### Frontend
```bash
cd client
npm install
npm start
```

## Notes
- The backend uses Spotify Client Credentials flow; for user-level features (playlists, personalization) you'd need OAuth.
- The recommender is intentionally simple (recommendations endpoint + clustering). Replace clustering logic with your own models for production.
