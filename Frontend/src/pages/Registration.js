import React, {useState} from 'react';
import {Button, Form, Input, Select, Space, Typography} from 'antd';
import axios from "axios";
import {useNavigate} from 'react-router-dom';

const {Option} = Select;
const { Title, Text } = Typography;

const RegistrationForm = () => {
    const navigate = useNavigate();
    const [role, setRole] = useState('receiver');

    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token !== null) {
        navigate('/home');
    }

    const onFinish = async (values) => {
        console.log('Received values:', values);

        // Validate data before sending
        if (!values.username || !values.password || !values.first_name || !values.last_name || !values.email || !values.role || !values.phone_number) {
            console.log('Missing required fields');
            return;
        }

        try {
            // Send post request to backend
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'}/account/register`, {
                username: values.username,
                password: values.password,
                first_name: values.first_name,
                last_name: values.last_name,
                email: values.email,
                role: values.role,
                phone_number: values.phone_number,
            });

            console.log(response);
            // message.success('Registration successful!');

            // If role is 'donor', send postal_code to /location endpoint
            if (values.role === 'donor' && values.postal_code) {
                const locationResponse = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'}/location/`, {
                    username: values.username, postal_code: values.postal_code,
                });

                console.log(locationResponse);
                // message.success('Postal code sent successfully!');
            }
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div style={{
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

                <Form.Item
                    name="email"
                    label="Email"
                    rules={[{
                        required: true, message: 'Please input your email!',
                    },]}
                >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="role"
                    label="Role"
                    rules={[{
                        required: true, message: 'Please select your role!',
                    },]}
                >
                    <Select placeholder="Select a role" onChange={(value) => setRole(value)}>
                        <Option value="donor">Donor</Option>
                        <Option value="receiver">Receiver</Option>
                    </Select>
                </Form.Item>

                <Form.Item
                    name="phone_number"
                    label="Phone Number"
                    rules={[{
                        required: true, message: 'Please input your phone number!',
                    }, ...(process.env.NODE_ENV !== 'development' ? [{
                        pattern: /^(\+65)?[689]\d{7}$/, message: 'Please enter a valid Singapore phone number!',
                    }] : []),]}
                >
                    <Input/>
                </Form.Item>

                {role === 'donor' && (<Form.Item
                    name="postal_code"
                    label="Postal Code"
                    rules={[{
                        required: true, message: 'Please input your postal code!',
                    },]}
                >
                    <Input/>
                </Form.Item>)}

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
        </Space>
    </div>);
};

export default RegistrationForm;