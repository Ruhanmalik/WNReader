import { Link } from 'react-router-dom'
import '../CSS/Navbar.css'

function Navbar() {
    return (
        <nav className='navbar'>
            <div className='navbar-links'>
                <Link to="/" className="nav-brand">
                WebNovel Reader
                </Link>
                <Link to='/URL' className='nav-link'>
                Search
                </Link>
            </div>

        </nav>
    );
}

export default Navbar;