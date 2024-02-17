import {useEffect} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import {message} from "antd";

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
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/logout/`, {}, {
                headers: {Authorization: `Bearer ${token}`}
            });

            // Check if the response status is 200 (OK)
            if (response.status === 200) {
                message.success(response.data.message);
                removeTokens();
                navigate('/login');
            } else {
                if (process.env.NODE_ENV === 'development') {
                    console.error('Failed to logout: Unexpected response status', response.status);
                }
            }
        } catch (error) {
            if (process.env.NODE_ENV === 'development') {
                console.error('Failed to logout:', error);
            }
            message.error('Failed to logout');
        }
    };

    useEffect(() => {
        logout();
    }, [navigate]);

    return null;
};

export default Logout;