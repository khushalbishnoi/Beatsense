import React from 'react';

export default function Hero() {
  return (
    <section style={{padding:'48px 0', background:'#fff'}}>
      <div className="container" style={{textAlign:'center'}}>
        <h1 style={{fontSize:34, margin:0}}>Beatsense — AI-driven Audio Recommendations</h1>
        <p style={{maxWidth:720, margin:'16px auto', color:'#334155'}}>Discover similar tracks and generate playlists using audio-feature based clustering and Spotify data.</p>
        <a href="/webapp" style={{display:'inline-block', padding:'10px 20px', background:'#0B3D91', color:'#fff', borderRadius:10}}>Try Beatsense</a>
      </div>
    </section>
  );
}
