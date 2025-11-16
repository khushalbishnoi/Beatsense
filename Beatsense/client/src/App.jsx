import React from 'react';
import Navbar from './Navbar';
import Hero from './Hero';
import Webapp from './Webapp';

export default function App() {
  // very small app router
  const path = window.location.pathname;
  return (
    <>
      <Navbar />
      {path === '/' && <Hero />}
      {path === '/webapp' && <Webapp />}
      {path !== '/' && path !== '/webapp' && <div className="container"><h2>404</h2></div>}
    </>
  );
}
