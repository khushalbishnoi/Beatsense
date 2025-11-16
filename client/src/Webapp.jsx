import React, { useState } from 'react';
import { searchTracks, getRecommendations } from './api';

export default function Webapp() {
  const [q, setQ] = useState("");
  const [tracks, setTracks] = useState([]);
  const [selected, setSelected] = useState([]);
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);

  async function doSearch(e) {
    e && e.preventDefault();
    if (!q) return;
    setLoading(true);
    const t = await searchTracks(q, 12);
    setTracks(t);
    setLoading(false);
  }

  function toggleSelect(id) {
    setSelected(s => s.includes(id) ? s.filter(x=>x!==id) : [...s, id]);
  }

  async function buildRecs() {
    if (selected.length === 0) return alert("Select at least one seed track");
    setLoading(true);
    const r = await getRecommendations(selected, 8);
    setRecs(r);
    setLoading(false);
  }

  return (
    <main style={{Padding:'24px 0'}}>
      <div className="container">
        <form onSubmit={doSearch} style={{display:'flex', gap:12, marginBottom:16}}>
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search for a track or artist" style={{flex:1, padding:10, borderRadius:8, border:'1px solid #dbeafe'}} />
          <button type="submit" style={{padding:'10px 16px', borderRadius:8, background:'#0B3D91', color:'#fff'}}>Search</button>
        </form>

        <section>
          <h3>Results</h3>
          <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))', gap:12}}>
            {tracks.map(t => (
              <div key={t.id} style={{padding:12, borderRadius:8, background:'#fff', boxShadow:'0 1px 3px rgba(15,23,42,0.06)'}}>
                <div style={{display:'flex', gap:12}}>
                  <img src={t.image || ''} alt="" style={{width:64, height:64, objectFit:'cover', borderRadius:6}} />
                  <div style={{flex:1}}>
                    <div style={{fontWeight:600}}>{t.name}</div>
                    <div style={{color:'#64748b', fontSize:13}}>{(t.artists || []).join(', ')}</div>
                  </div>
                </div>
                <div style={{marginTop:8, display:'flex', gap:8}}>
                  <button onClick={()=>toggleSelect(t.id)} style={{padding:'6px 10px', borderRadius:8, border:'1px solid #e2e8f0', background: selected.includes(t.id) ? '#0B3D91' : '#fff', color: selected.includes(t.id) ? '#fff' : '#0b2745'}}> {selected.includes(t.id) ? 'Selected' : 'Select'} </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div style={{marginTop:18}}>
          <button onClick={buildRecs} style={{padding:'10px 14px', background:'#0B3D91', color:'#fff', borderRadius:8}}>Generate Recommendations</button>
        </div>

        <section style={{marginTop:20}}>
          <h3>Recommendations</h3>
          <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))', gap:12}}>
            {recs.map(r => (
              <div key={r.id} style={{padding:12, borderRadius:8, background:'#fff'}}>
                <div style={{display:'flex', gap:12}}>
                  <img src={r.image || ''} alt="" style={{width:64, height:64, objectFit:'cover', borderRadius:6}} />
                  <div>
                    <div style={{fontWeight:600}}>{r.name}</div>
                    <div style={{color:'#64748b', fontSize:13}}>{(r.artists || []).join(', ')}</div>
                  </div>
                </div>
                {r.preview_url && <audio controls src={r.preview_url} style={{width:'100%', marginTop:8}} />}
              </div>
            ))}
            {recs.length === 0 && <div style={{color:'#94a3b8'}}>No recommendations yet — pick seeds and click "Generate Recommendations".</div>}
          </div>
        </section>
      </div>
    </main>
  );
}
