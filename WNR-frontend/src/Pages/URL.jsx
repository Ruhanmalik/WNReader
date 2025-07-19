import Input from '../components/Input.jsx'
import '../CSS/URL.css'
import { useState, useEffect } from 'react'
import axios from 'axios'

function URL() {
    return (
        <div className="url-page">
            <h1>Convert Web Novel to Audio</h1>
            <div className="url-content">
                <Input />
            </div>
        </div>
    )
}

export default URL