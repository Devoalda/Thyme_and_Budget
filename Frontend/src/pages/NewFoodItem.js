import React from 'react';
import {Button, DatePicker, Form, Input, message, Space, Typography, Upload} from 'antd';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import LayoutComponent from '../components/Layout';

const {Title, Text} = Typography;

const NewFoodItem = () => {
    const navigate = useNavigate();

    const onFinish = async (values) => {
        try {
            // Convert image file to base64 string
            const reader = new FileReader();
            reader.readAsDataURL(values.image.fileList[0].originFileObj);
            reader.onloadend = async () => {
                const base64Image = reader.result.split(',')[1];

                // Get the token from local storage
                const token = localStorage.getItem('token');

                // Send post request to backend
                const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/food/`, {
                    name: values.name,
                    expiry_date: values.expiry_date.format('YYYY-MM-DD'),
                    quantity: values.quantity,
                    image: base64Image,
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                message.success('Food item created successfully!');
                navigate('/home');
            };
        } catch (error) {
            if (process.env.NODE_ENV === 'development') {
                console.log(error);
            }
            message.error('Failed to create food item');
        }
    };

    return (<LayoutComponent>
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
                    name="newFoodItem"
                    onFinish={onFinish}
                    initialValues={{remember: true}}
                    scrollToFirstError
                >
                    <Form.Item
                        name="name"
                        rules={[{required: true, message: 'Please input the food item name!'}]}
                    >
                        <Input placeholder="Name"/>
                    </Form.Item>

                    <Form.Item
                        name="expiry_date"
                        rules={[{required: true, message: 'Please input the expiry date!'}]}
                    >
                        <DatePicker placeholder="Expiry Date"/>
                    </Form.Item>

                    <Form.Item
                        name="quantity"
                        rules={[{required: true, message: 'Please input the quantity!'}]}
                    >
                        <Input type="number" placeholder="Quantity"/>
                    </Form.Item>

                    <Form.Item
                        name="image"
                        rules={[{required: true, message: 'Please upload an image!'}]}
                    >
                        <Upload
                            name="image"
                            listType="picture"
                            beforeUpload={(file) => {
                                // Prevent the Upload component from uploading the file automatically
                                return false;
                            }}
                        >
                            <Button>Click to upload</Button>
                        </Upload>
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Space>
        </div>
    </LayoutComponent>);
};

export default NewFoodItem;