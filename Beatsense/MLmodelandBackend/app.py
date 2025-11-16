# app.py
import os
from flask import Flask, jsonify, request
from spotify_client import SpotifyClient
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Read credentials from environment (set via .env or Docker)
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    # App will still run for local dev without Spotify; endpoints will return guidance.
    spotify = None
else:
    spotify = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/api/search")
def search():
    """Search tracks by query (uses Spotify search)."""
    q = request.args.get("q", "")
    limit = int(request.args.get("limit", 12))
    if not spotify:
        return jsonify(error="Spotify credentials not configured. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET."), 400
    data = spotify.get("/search", params={"q": q, "type": "track", "limit": limit})
    tracks = []
    for item in data.get("tracks", {}).get("items", []):
        tracks.append({
            "id": item["id"],
            "name": item["name"],
            "artists": [a["name"] for a in item.get("artists", [])],
            "album": item.get("album", {}).get("name"),
            "preview_url": item.get("preview_url"),
            "image": (item.get("album", {}).get("images") or [{}])[0].get("url")
        })
    return jsonify(tracks=tracks)

@app.route("/api/features")
def features():
    """Fetch audio features for a list of track ids (comma-separated)."""
    ids = request.args.get("ids", "")
    if not ids:
        return jsonify(error="Provide ids param (comma-separated track ids)"), 400
    if not spotify:
        return jsonify(error="Spotify credentials not configured."), 400
    ids = ids.split(",")
    data = spotify.get("/audio-features", params={"ids": ",".join(ids)})
    return jsonify(data=data.get("audio_features", []))

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Simple recommender:
    - Accepts a JSON body with 'seed_track_ids': [id1,id2,...]
    - Strategy:
       1. For each seed, fetch related tracks via "recommendations" endpoint
       2. Collect audio features, apply KMeans clustering (k=3)
       3. Return tracks from cluster closest to seed(s)
    """
    body = request.get_json(force=True, silent=True) or {}
    seed_ids = body.get("seed_track_ids", [])
    max_recs = int(body.get("max_recs", 10))
    if not seed_ids:
        return jsonify(error="Send seed_track_ids in JSON body."), 400
    if not spotify:
        return jsonify(error="Spotify credentials not configured."), 400

    # Step 1: Get recommendations for each seed
    recs = []
    for sid in seed_ids:
        try:
            data = spotify.get("/recommendations", params={"seed_tracks": sid, "limit": 20})
            for t in data.get("tracks", []):
                recs.append(t)
        except Exception:
            continue

    # dedupe by id
    by_id = {}
    for t in recs:
        by_id[t["id"]] = t
    recs = list(by_id.values())[:200]

    # Step 2: get audio features
    track_ids = [t["id"] for t in recs]
    features = []
    BATCH = 50
    for i in range(0, len(track_ids), BATCH):
        batch = track_ids[i:i+BATCH]
        data = spotify.get("/audio-features", params={"ids": ",".join(batch)})
        features.extend(data.get("audio_features", []))

    # filter out None features
    valid = []
    valid_tracks = []
    for t,f in zip(recs, features):
        if f and isinstance(f, dict):
            # choose numeric audio features relevant for clustering
            vec = [
                f.get("danceability", 0),
                f.get("energy", 0),
                f.get("valence", 0),
                f.get("tempo", 0) / 300.0,  # normalize tempo
                f.get("speechiness", 0),
                f.get("acousticness", 0)
            ]
            valid.append(vec)
            valid_tracks.append({"track": t, "features": f})

    if not valid:
        return jsonify(recommendations=[])

    X = np.array(valid)

    # Step 3: KMeans clustering
    k = min(3, max(1, X.shape[0]//10))
    try:
        km = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)
        labels = km.labels_
    except Exception:
        labels = [0] * len(valid_tracks)

    # choose cluster that contains most similar items to seeds (approx: cluster of first seed rec)
    chosen_cluster = labels[0] if labels else 0
    picks = []
    for lt,lab in zip(valid_tracks, labels):
        if lab == chosen_cluster:
            t = lt["track"]
            picks.append({
                "id": t["id"],
                "name": t["name"],
                "artists": [a["name"] for a in t.get("artists", [])],
                "album": t.get("album", {}).get("name"),
                "image": (t.get("album", {}).get("images") or [{}])[0].get("url"),
                "preview_url": t.get("preview_url")
            })
            if len(picks) >= max_recs:
                break

    return jsonify(recommendations=picks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
