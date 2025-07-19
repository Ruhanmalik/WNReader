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

    const getMessageClass = () => {
        if (message.includes('Error') || message.includes('error')) {
            return 'message error';
        } else if (message.includes('success') || message.includes('Success')) {
            return 'message success';
        } else {
            return 'message info';
        }
    }

    return (
        <div className="input-container">
            <form className="input-form" onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    placeholder="Enter Novelhi.com URL here..." 
                    className="url-input"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                />
                <button 
                    type="submit" 
                    className="submit-button" 
                    disabled={loading}
                >
                    {loading && <span className="loading-spinner"></span>}
                    {loading ? 'Processing...' : 'Convert to Audio'}
                </button>
            </form>
            
            {message && <p className={getMessageClass()}>{message}</p>}
            
            <div className="audio-container">
                {!audioExists && <p className="no-audio">No audio file available</p>}
                {audioExists && <audio src={audioUrl} controls className="audio-player"></audio>}
            </div>
        </div>
    )
}

export default Input