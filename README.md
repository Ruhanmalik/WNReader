# 📚 WebNovel Reader

A modern web application that converts web novels from Novelhi.com into high-quality audiobooks using advanced text-to-speech technology. (Current Time only works with LOTM will add a tag setter soon)

![WebNovel Reader](https://img.shields.io/badge/React-19.1.0-blue)
![WebNovel Reader](https://img.shields.io/badge/Python-3.8+-green)
![WebNovel Reader](https://img.shields.io/badge/Flask-3.1.1-red)

## ✨ Features

- **🎤 High-Quality TTS**: Uses Kokoro TTS for natural-sounding audio generation
- **🌐 Web Scraping**: Automatically extracts novel content from Novelhi.com URLs
- **🎨 Modern UI**: Clean, responsive design with glassmorphism effects
- **⚡ Real-time Processing**: Live audio status updates and streaming
- **📱 Mobile Responsive**: Works seamlessly on all devices
- **🎯 Easy to Use**: Simple URL input with one-click conversion

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **FFmpeg** (for audio processing)
- **Git**

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd WNReader
   ```

2. **Install FFmpeg**

   **macOS:**

   ```bash
   brew install ffmpeg
   ```

   **Ubuntu/Debian:**

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   **Windows:**
   Download from [FFmpeg official website](https://ffmpeg.org/download.html)

3. **Setup Frontend**

   ```bash
   cd WNR-frontend
   npm install
   npm install react-router-dom
   ```

4. **Setup Backend**

   ```bash
   cd ../backend
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

### Start the Backend Server

```bash
cd backend
# Activate virtual environment if not already activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

python app.py
```

The backend server will start on `http://127.0.0.1:5000`

### Start the Frontend Development Server

```bash
cd WNR-frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🎯 Usage

1. **Navigate to the application** in your browser
2. **Enter a Novelhi.com URL** in the input field
3. **Click "Convert to Audio"** to start the conversion process
4. **Wait for processing** - the system will scrape the novel content and generate audio
5. **Play the generated audio** using the built-in audio player

## 🏗️ Project Structure

```
WNReader/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── webScrape.py       # Web scraping utilities
│   └── venv/              # Python virtual environment
├── WNR-frontend/          # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── Pages/         # Page components
│   │   ├── CSS/           # Stylesheets
│   │   └── App.jsx        # Main app component
│   ├── package.json       # Node.js dependencies
│   └── index.html         # HTML template
└── README.md              # This file
```

## 🔧 API Endpoints

### Backend API (Flask)

- `POST /api/url` - Submit a URL for processing
- `GET /api/audio` - Download the generated audio file
- `GET /api/audio/status` - Check audio file status

### Frontend Routes (React Router)

- `/` - Home page with welcome message
- `/URL` - URL input and audio conversion page

## 🛠️ Technologies Used

### Frontend

- **React 19.1.0** - Modern UI framework
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **Vite** - Fast build tool and dev server
- **CSS3** - Modern styling with glassmorphism effects

### Backend

- **Flask 3.1.1** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Kokoro TTS** - Advanced text-to-speech engine
- **BeautifulSoup4** - Web scraping library
- **FFmpeg** - Audio processing and concatenation
- **PyTorch** - Machine learning framework for TTS

## 🎨 Design Features

- **Glassmorphism UI** - Modern translucent design elements
- **Neutral Color Palette** - Professional gray and white theme
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Smooth Animations** - Hover effects and transitions
- **Loading States** - Visual feedback during processing
- **Error Handling** - User-friendly error messages

## 🔍 How It Works

1. **URL Submission**: User enters a Novelhi.com URL
2. **Web Scraping**: Backend extracts novel content using BeautifulSoup
3. **Text Processing**: Content is cleaned and formatted for TTS
4. **Audio Generation**: Kokoro TTS converts text to high-quality audio
5. **File Management**: Audio chunks are combined using FFmpeg
6. **Streaming**: Frontend polls for audio status and streams the result

## 🚨 Troubleshooting

### Common Issues

**FFmpeg not found:**

```bash
# Ensure FFmpeg is installed and in your PATH
ffmpeg -version
```

**Python dependencies issues:**

```bash
# Reinstall requirements in a fresh virtual environment
python -m venv new_venv
source new_venv/bin/activate
pip install -r requirements.txt
```

**Audio generation fails:**

- Check that the URL is from Novelhi.com
- Ensure sufficient disk space for audio files
- Verify FFmpeg installation

**Frontend build issues:**

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kokoro TTS** for providing high-quality text-to-speech capabilities
- **Novelhi.com** for hosting web novels
- **React** and **Flask** communities for excellent documentation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [issues](../../issues)
3. Create a new issue with detailed information

---

**Made with ❤️ for web novel enthusiasts**
