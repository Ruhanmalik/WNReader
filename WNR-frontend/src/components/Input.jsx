import '../CSS/Input.css'
import {useState, useEffect } from 'react'
import axios from 'axios'

function Input() {

    const [url, setUrl] = useState('')
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)
    const [audioUrl, setAudioUrl] = useState('http://127.0.0.1:5000/api/audio')
    const [audioExists, setAudioExists] = useState(false)
    const [audioTimestamp, setAudioTimestamp] = useState(null)

    // Poll for audio file status
    useEffect(() => {
        const checkAudioStatus = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/audio/status');
                const { exists, timestamp } = response.data;
                
                if (exists !== audioExists || timestamp !== audioTimestamp) {
                    setAudioExists(exists);
                    setAudioTimestamp(timestamp);
                    if (exists) {
                        // Update audio URL with timestamp to force reload
                        setAudioUrl(`http://127.0.0.1:5000/api/audio?t=${Date.now()}`);
                    }
                }
            } catch (error) {
                console.error('Error checking audio status:', error);
            }
        };

        // Check immediately
        checkAudioStatus();

        // Set up polling every 2 seconds
        const interval = setInterval(checkAudioStatus, 2000);

        return () => clearInterval(interval);
    }, [audioExists, audioTimestamp]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

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
            <br></br>
            {message && <p className="message">{message}</p>}
            {!audioExists && <p>No audio file available</p>}
            {audioExists && <audio src={audioUrl} controls></audio>}
        </div>
    )
}

export default Input