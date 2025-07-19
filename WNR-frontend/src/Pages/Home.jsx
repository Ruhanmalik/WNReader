import '../CSS/Home.css'

function Home() {
    return (
        <div className="home-page">
            <div className="home-content">
                <h1>Welcome to WebNovel Reader</h1>
                <p>Enter a URL from Novelhi.com to turn your favorite web novel chapter into audiobooks!</p>
                
                <div className="feature-list">
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>Convert web novels to high-quality audio</span>
                    </div>
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>Easy-to-use interface</span>
                    </div>
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>Fast processing and streaming</span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home