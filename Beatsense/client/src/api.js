// api.js - small wrapper to backend API
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "/api";

export async function searchTracks(q, limit=12) {
  const res = await axios.get(`${API_BASE}/search`, { params: { q, limit }});
  return res.data.tracks || [];
}

export async function getRecommendations(seedIds, max_recs=8) {
  const res = await axios.post(`${API_BASE}/recommend`, { seed_track_ids: seedIds, max_recs });
  return res.data.recommendations || [];
}
