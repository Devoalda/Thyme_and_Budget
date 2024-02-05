import { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const TOKEN_KEY = 'token';
const REFRESH_KEY = 'refresh';

const Logout = () => {
    const navigate = useNavigate();

    const removeTokens = () => {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
    };

    const logout = async () => {
        const token = localStorage.getItem(TOKEN_KEY);
        try {
            await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/account/logout`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            removeTokens();
            navigate('/login');
        } catch (error) {
            console.error('Failed to logout:', error);
            removeTokens();
            navigate('/login');
        }
    };

    useEffect(() => {
        logout();
    }, [navigate]);

    return null;
};

export default Logout;