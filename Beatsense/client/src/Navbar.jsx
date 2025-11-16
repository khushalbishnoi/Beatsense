import React from 'react';

export default function Navbar() {
  return (
    <header style={{ background: "#ffffff", borderBottom: "1px solid #e6eef8" }}>
      <div className="container" style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <div style={{fontSize:20, fontWeight:700, color:"#0B3D91"}}>Beatsense</div>
        <nav>
          <a href="/" style={{marginRight:12}}>Home</a>
          <a href="/webapp">Web App</a>
        </nav>
      </div>
    </header>
  );
}
