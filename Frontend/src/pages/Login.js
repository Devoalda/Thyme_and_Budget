import React from 'react';
import {useNavigate} from 'react-router-dom';
import {Button, Form, Input, message} from 'antd';
import axios from "axios";

const Login = () => {
    const navigate = useNavigate();

    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token !== null) {
        window.location.href = '/home';
    }

    const onFinish = (values) => {
        // Send post request to backend
        axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/token/`, {
            username: values.username, password: values.password,
        })
            .then((response) => {
                setTimeout(() => {
                    // Save tokens to local storage
                    localStorage.setItem('token', response.data.access);
                    localStorage.setItem('refresh', response.data.refresh);
                }, 1000);
                // Redirect to home page
                navigate('/home');
            }, (error) => {
                console.log(error);
                message.error('Failed to login. Please try again.');
            });
    };

    return (<div style={{width: '300px', margin: 'auto'}}>
        <Form
            name="login"
            onFinish={onFinish}
            initialValues={{remember: true}}
            scrollToFirstError
        >
            <h1 style={{textAlign: 'center'}}>Login</h1>

            <Form.Item
                name="username"
                label="Username"
                rules={[{
                    required: true, message: 'Please input your username!',
                },]}
            >
                <Input/>
            </Form.Item>

            <Form.Item
                name="password"
                label="Password"
                rules={[{
                    required: true, message: 'Please input your password!',
                },]}
            >
                <Input.Password/>
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                    Login
                </Button>
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="button" style={{width: '100%'}}
                        onClick={() => navigate('/')}>
                    Register
                </Button>
            </Form.Item>
        </Form>
    </div>);
};

export default Login;