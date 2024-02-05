import React from 'react';
import {useNavigate} from 'react-router-dom';
import {Form, Input, Button, message} from 'antd';
import axios from "axios";

const Login = () => {
    const navigate = useNavigate();
    const onFinish = (values) => {
        // Send post request to backend
        axios.post('http://127.0.0.1:8000/api/token/', {
            username: values.username,
            password: values.password,
        })
            .then((response) => {
                setTimeout(() => {
                    //console.log(response);
                    // Save tokens to local storage
                    localStorage.setItem('token', response.data.access);
                    localStorage.setItem('refresh', response.data.refresh);
                    //console.log('Token:', response.data.access);
                    //console.log('Refresh:', response.data.refresh);
                }, 1000);
                // Redirect to home page
                navigate('/home');
            }, (error) => {
                console.log(error);
                message.error('Failed to login. Please try again.');
            });
    };

    return (
        <div style={{width: '300px', margin: 'auto'}}>
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
                    rules={[
                        {
                            required: true,
                            message: 'Please input your username!',
                        },
                    ]}
                >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="password"
                    label="Password"
                    rules={[
                        {
                            required: true,
                            message: 'Please input your password!',
                        },
                    ]}
                >
                    <Input.Password/>
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        Login
                    </Button>
                </Form.Item>
                <Form.Item>
                    <Button type="link" htmlType="button" style={{width: '100%'}} href="/">
                        Register
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default Login;
