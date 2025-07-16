import Input from '../components/Input.jsx'
import '../CSS/URL.css'
import { useState, useEffect } from 'react'
import axios from 'axios'

function URL() {
    return (
        <div className="url-page">
            <h1>URL</h1>
            <Input />
        </div>
    )
}

export default URL