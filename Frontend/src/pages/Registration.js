import React, {useState} from 'react';
import {Button, Form, Input, message, Select, Space, Typography} from 'antd';
import axios from "axios";
import {useNavigate} from 'react-router-dom';

const {Option} = Select;
const {Title, Text} = Typography;

// Function to handle form validation rules
const getValidationRules = (field) => {
    switch (field) {
        case 'username':
        case 'password':
        case 'first_name':
        case 'last_name':
        case 'email':
        case 'role':
        case 'phone_number':
            return [{required: true, message: `Please input your ${field}!`}];
        case 'confirm':
            return [{
                required: true, message: 'Please confirm your password!',
            }, ({getFieldValue}) => ({
                validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                    }
                    return Promise.reject('The two passwords do not match!');
                },
            })];
        default:
            return [];
    }
};

// Function to handle form fields
const getFormField = (name, label, children) => {
    return (<Form.Item
            name={name}
            label={label}
            rules={getValidationRules(name)}
        >
            {children}
        </Form.Item>);
};

// Function to handle form buttons
const getFormButton = (type, htmlType, text, style = {width: '100%'}) => {
    return (<Form.Item>
            <Button type={type} htmlType={htmlType} style={style}>
                {text}
            </Button>
        </Form.Item>);
};

// Main function
const RegistrationForm = () => {
    const navigate = useNavigate();
    const [role, setRole] = useState('receiver');

    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token !== null) {
        navigate('/home');
    }

    const onFinish = async (values) => {
        // Validate data before sending
        if (!values.username || !values.password || !values.first_name || !values.last_name || !values.email || !values.role || !values.phone_number) {
            message.error('Missing required fields');
            return;
        }

        try {
            // Send post request to backend
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'}/register/`, {
                username: values.username,
                password: values.password,
                first_name: values.first_name,
                last_name: values.last_name,
                email: values.email,
                role: values.role,
                phone_number: values.phone_number,
            });

            // If role is 'donor', send postal_code to /location endpoint
            if (values.role === 'donor' && values.postal_code) {
                const locationResponse = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'}/location/`, {
                    username: values.username, postal_code: values.postal_code,
                });

                if (process.env.NODE_ENV === 'development') {
                    console.log(locationResponse);
                }
            }

            message.success('Account created successfully! Redirecting to login page...');
            setTimeout(() => {
                navigate('/login');
            }, 3000);

        } catch (error) {
            if (error.response) {
                for (const [key, value] of Object.entries(error.response.data)) {
                    message.error(`${key}: ${value}`);
                }
            } else if (error.request) {
                message.error('Network error');
                if (process.env.NODE_ENV === 'development') {
                    console.log(error.request);
                }
            } else {
                message.error('Unknown error');
                if (process.env.NODE_ENV === 'development') {
                    console.log(error.config);
                }
            }
            if (process.env.NODE_ENV === 'development') {
                console.log(error.config);
            }
        }
    };

    return (<div style={{
            width: '300px',
            margin: 'auto',
            padding: '20px',
            backgroundColor: '#f8f9fa',
            borderRadius: '10px',
            boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)'
        }}>
            <Space direction="vertical" size="large" style={{width: '100%'}}>
                <Title level={2} style={{textAlign: 'center', color: '#343a40'}}>Thyme and Budget</Title>
                <Text style={{textAlign: 'center', color: '#6c757d'}}>Share food, save the planet</Text>
                <Form
                    name="register"
                    onFinish={onFinish}
                    initialValues={{remember: true, role: 'receiver'}}
                    scrollToFirstError
                >
                    <h1 style={{textAlign: 'center', color: '#333'}}>Registration</h1>

                    {getFormField("username", "Username", <Input/>)}
                    {getFormField("password", "Password", <Input.Password/>)}
                    {getFormField("confirm", "Confirm Password", <Input.Password/>)}
                    {getFormField("first_name", "First Name", <Input/>)}
                    {getFormField("last_name", "Last Name", <Input/>)}
                    {getFormField("email", "Email", <Input/>)}
                    {getFormField("role", "Role", <Select placeholder="Select a role"
                                                          onChange={(value) => setRole(value)}>
                        <Option value="donor">Donor</Option>
                        <Option value="receiver">Receiver</Option>
                    </Select>)}
                    {getFormField("phone_number", "Phone Number", <Input/>)}
                    {role === 'donor' && getFormField("postal_code", "Postal Code", <Input/>)}

                    {getFormButton("primary", "submit", "Register")}
                </Form>
                <Button type="primary" htmlType="button" style={{width: '100%'}}
                        onClick={() => navigate('/login')}>
                    Login
                </Button>
            </Space>
        </div>);
};

export default RegistrationForm;