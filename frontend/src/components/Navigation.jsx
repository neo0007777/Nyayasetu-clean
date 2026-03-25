import { useState, useRef, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Scale, BookOpen, MessageSquare, Home as HomeIcon, FileSearch, Clock, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import './Navigation.css';

const Navigation = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleLogout = () => {
        setIsDropdownOpen(false);
        logout();
    };

    return (
        <aside className="sidebar-nav">
            <div className="sidebar-header">
                <div className="logo-icon"><Scale size={20} /></div>
                <div className="logo-text">
                    <h2>NyayaSetu</h2>
                    <span className="badge">PRO</span>
                </div>
            </div>

            <div className="sidebar-section">
                <p className="section-title">Workspace</p>
                <div className="nav-links">
                    <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                        <HomeIcon size={18} /> Dashboard
                    </NavLink>
                    <NavLink to="/case-finder" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                        <Scale size={18} /> Case Finder
                    </NavLink>
                    <NavLink to="/draft-assistant" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                        <BookOpen size={18} /> Draft Assistant
                    </NavLink>
                    <NavLink to="/clause-conflict" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                        <FileSearch size={18} /> Contract Analysis
                    </NavLink>
                    <NavLink to="/legal-aid" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                        <MessageSquare size={18} /> AI Legal Aid
                    </NavLink>
                </div>
            </div>

            <div className="sidebar-section mt-auto">
                <p className="section-title">Recent Activity</p>
                <div className="recent-list">
                    <div className="recent-item"><Clock size={14} /> Case Search</div>
                    <div className="recent-item"><Clock size={14} /> Draft Assistant</div>
                    <div className="recent-item"><Clock size={14} /> Legal Aid Q&A</div>
                </div>
            </div>

            <div className="sidebar-footer">
                {user ? (
                    <div className="authenticated-user-container" ref={dropdownRef}>
                        <div className="dynamic-user-profile" onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
                            <div className="avatar">
                                {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                            </div>
                            <div className="user-info">
                                <strong>{user.name || 'User'}</strong>
                                <span>{user.plan || 'Member'}</span>
                            </div>
                        </div>

                        {isDropdownOpen && (
                            <div className="profile-dropdown animate-fade-up">
                                <div className="dropdown-user-header">
                                    <strong>{user.name}</strong>
                                    <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>{user.email}</span>
                                </div>
                                <div className="dropdown-divider"></div>
                                <button className="dropdown-action text-red-600" onClick={handleLogout}>
                                    <LogOut size={16} /> Logout
                                </button>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="unauthenticated-container">
                        <button className="massive-login-btn" onClick={() => navigate('/login')}>
                            <User size={18} /> Login / Sign Up
                        </button>
                    </div>
                )}
            </div>
        </aside>
    );
};

export default Navigation;
