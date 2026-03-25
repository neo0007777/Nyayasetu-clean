import React, { useState } from 'react';
import { Shield, Lock, Mail, ArrowRight, AlertCircle, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login = () => {
    const [tab, setTab] = useState('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [role, setRole] = useState('advocate');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const { login, register } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        let result;
        if (tab === 'login') {
            result = await login(email, password);
        } else {
            if (!fullName.trim()) {
                setError('Full name is required.');
                setIsLoading(false);
                return;
            }
            result = await register(fullName, email, password, role);
        }

        if (!result.success) {
            setError(result.message);
            setIsLoading(false);
        }
    };

    return (
        <div className="login-matrix">
            <div className="login-graphic-panel">
                <div className="logo-vertical">
                    <Shield size={64} className="text-blue-500 mb-4" />
                    <h1>NyayaSetu</h1>
                    <p>Enterprise Legal Intelligence</p>
                </div>
                <div className="graphic-features">
                    <div className="graphic-item">
                        <div className="g-icon"><Lock size={18} /></div>
                        <span>End-to-end AES-256 Document Encryption</span>
                    </div>
                    <div className="graphic-item">
                        <div className="g-icon"><Shield size={18} /></div>
                        <span>JWT Secured Authentication</span>
                    </div>
                </div>
            </div>

            <div className="login-interactive-panel">
                <div className="login-card">
                    <div className="login-tabs">
                        <button
                            className={`login-tab ${tab === 'login' ? 'active' : ''}`}
                            onClick={() => { setTab('login'); setError(''); }}
                        >
                            Sign In
                        </button>
                        <button
                            className={`login-tab ${tab === 'register' ? 'active' : ''}`}
                            onClick={() => { setTab('register'); setError(''); }}
                        >
                            Register
                        </button>
                    </div>

                    <h2>{tab === 'login' ? 'Welcome back' : 'Create Account'}</h2>
                    <p className="login-subtitle">
                        {tab === 'login'
                            ? 'Enter your credentials to access the workspace.'
                            : 'Join NyayaSetu to get started.'}
                    </p>

                    {error && (
                        <div className="login-error-flag animate-fade-in">
                            <AlertCircle size={18} />
                            <span>{error}</span>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="login-form">
                        {tab === 'register' && (
                            <div className="input-group">
                                <label>Full Name</label>
                                <div className="input-wrapper">
                                    <User size={18} className="input-icon" />
                                    <input
                                        type="text"
                                        placeholder="e.g. Advocate Sharma"
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>
                        )}

                        <div className="input-group">
                            <label>Email Address</label>
                            <div className="input-wrapper">
                                <Mail size={18} className="input-icon" />
                                <input
                                    type="email"
                                    placeholder="advocate@example.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        <div className="input-group">
                            <div className="label-row">
                                <label>Password</label>
                            </div>
                            <div className="input-wrapper">
                                <Lock size={18} className="input-icon" />
                                <input
                                    type="password"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        {tab === 'register' && (
                            <div className="input-group">
                                <label>Role</label>
                                <div className="input-wrapper">
                                    <select
                                        value={role}
                                        onChange={(e) => setRole(e.target.value)}
                                        style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', background: 'transparent', border: 'none', outline: 'none' }}
                                    >
                                        <option value="advocate">Advocate</option>
                                        <option value="intern">Legal Intern</option>
                                        <option value="user">User</option>
                                    </select>
                                </div>
                            </div>
                        )}

                        <button
                            type="submit"
                            className={`login-submit-btn ${isLoading ? 'loading' : ''}`}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Authenticating...' : (
                                <>{tab === 'login' ? 'Sign in' : 'Create Account'} <ArrowRight size={18} /></>
                            )}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
