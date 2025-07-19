import { useState, useEffect } from 'react'
import './CSS/App.css'
import axios from 'axios'
import {Routes, Route} from 'react-router-dom'
import Home from './Pages/Home'
import URL from './Pages/URL'
import Navbar from './components/Navbar'

function App() {
  return (
    <div>
      <main className='main-content'>
        <Navbar />
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/URL" element={<URL />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}

export default App
