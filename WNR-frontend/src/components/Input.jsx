import '../CSS/Input.css'
import {useState, useEffect } from 'react'
import axios from 'axios'

function Input() {

    const [url, setUrl] = useState('')
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        setLoading(true)
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/url', {url:url});
            setMessage(response.data.message)
        } catch (error) {
            if (error.response) {
                setMessage(error.response.data.message || "Server Error Occured");
            }
            else if (error.request) {
                setMessage("No Response from Server");
            }
            else {
                setMessage("An error occured while making the request");
            }
        } finally {
            setLoading(false)
        }
    }
    return (
        <div className="input-container">
            <input 
                type="text" 
                placeholder="Enter URL" 
                className="url-input"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? 'Processing...' : 'Submit'}
            </button>
            {message && <p className="message">{message}</p>}
        </div>
    )
}

export default Input