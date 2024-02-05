import React from 'react';
import {Button, Form, Input, message} from 'antd';
import axios from "axios";
import {useNavigate} from 'react-router-dom';

const RegistrationForm = () => {
    const navigate = useNavigate();

    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token !== null) {
        navigate('/home');
    }

    const onFinish = (values) => {
        console.log('Received values:', values);
        // Send post request to backend
        axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'}/account/register`, {
            username: values.username,
            password: values.password,
            first_name: values.first_name,
            last_name: values.last_name,
        })
            .then((response) => {
                setTimeout(() => {
                    console.log(response);
                    message.success('Registration successful!');
                }, 1000);

            }, (error) => {
                console.log(error);
            });
    };

    return (<div style={{width: '300px', margin: 'auto'}}>
            <Form
                name="register"
                onFinish={onFinish}
                initialValues={{remember: true}}
                scrollToFirstError
            >
                <h1 style={{textAlign: 'center'}}>Registration</h1>

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
                    hasFeedback
                >
                    <Input.Password/>
                </Form.Item>

                <Form.Item
                    name="confirm"
                    label="Confirm Password"
                    dependencies={['password']}
                    hasFeedback
                    rules={[{
                        required: true, message: 'Please confirm your password!',
                    }, ({getFieldValue}) => ({
                        validator(_, value) {
                            if (!value || getFieldValue('password') === value) {
                                return Promise.resolve();
                            }
                            return Promise.reject('The two passwords do not match!');
                        },
                    }),]}
                >
                    <Input.Password/>
                </Form.Item>

                <Form.Item
                    name="first_name"
                    label="First Name"
                    rules={[{
                        required: true, message: 'Please input your first name!',
                    },]}
                >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="last_name"
                    label="Last Name"
                    rules={[{
                        required: true, message: 'Please input your last name!',
                    },]}
                >
                    <Input/>
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        Register
                    </Button>
                </Form.Item>

                <Form.Item>
                    <Button type="default" href={'/login'} htmlType="button" style={{width: '100%'}}>
                        Login
                    </Button>
                </Form.Item>
            </Form>
        </div>);
};

export default RegistrationForm;