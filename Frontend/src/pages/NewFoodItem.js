import React from 'react';
import {Button, DatePicker, Form, Input, message, Space, Typography, Upload} from 'antd';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import LayoutComponent from '../components/Layout';

const {Title, Text} = Typography;

// Function to convert file to base64
const convertFileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
    });
};

// Function to post food item
const postFoodItem = async (values, base64Image) => {
    const token = localStorage.getItem('token');
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
    return response;
};

// Function to handle errors
const handleErrors = (error) => {
    if (error.response && error.response.status === 400) {
        // Bad request
        for (const [key, value] of Object.entries(error.response.data)) {
            message.error(`${key}: ${value}`);
        }
    } else {
        message.error('Failed to create food item');
        if (process.env.NODE_ENV === 'development') {
            console.log(error);
        }
    }
};

// Main function
const NewFoodItem = () => {
    const navigate = useNavigate();

    const onFinish = async (values) => {
        try {
            // Check if more than one file is uploaded
            if (values.image.fileList.length > 1) {
                message.error('You can only upload one file!');
                return;
            }

            // Convert image file to base64 string
            const base64Image = await convertFileToBase64(values.image.fileList[0].originFileObj);

            // Send post request to backend
            await postFoodItem(values, base64Image);

            message.success('Food item created successfully!');
            navigate('/home');
        } catch (error) {
            handleErrors(error);
        }
    };

    // Render function
    return (<LayoutComponent>
            <div style={styles.container}>
                <Space direction="vertical" size="large" style={{width: '100%'}}>
                    <Title level={2} style={styles.title}>Thyme and Budget</Title>
                    <Text style={styles.subtitle}>Share food, save the planet</Text>
                    <Form
                        name="newFoodItem"
                        onFinish={onFinish}
                        initialValues={{remember: true}}
                        scrollToFirstError
                    >
                        <Form.Item name="name" rules={[{required: true, message: 'Please input the food item name!'}]}>
                            <Input placeholder="Name"/>
                        </Form.Item>
                        <Form.Item name="expiry_date"
                                   rules={[{required: true, message: 'Please input the expiry date!'}]}>
                            <DatePicker placeholder="Expiry Date"/>
                        </Form.Item>
                        <Form.Item name="quantity" rules={[{required: true, message: 'Please input the quantity!'}]}>
                            <Input type="number" placeholder="Quantity"/>
                        </Form.Item>
                        <Form.Item name="image" rules={[{required: true, message: 'Please upload an image!'}]}>
                            <Upload
                                name="image"
                                listType="picture"
                                beforeUpload={beforeUpload}
                                onChange={onChange}
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

// Styles
const styles = {
    container: {
        width: '300px',
        margin: 'auto',
        padding: '20px',
        backgroundColor: '#f8f9fa',
        borderRadius: '10px',
        boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)'
    }, title: {
        textAlign: 'center', color: '#343a40'
    }, subtitle: {
        textAlign: 'center', color: '#6c757d'
    }
};

// Before upload function
const beforeUpload = (file) => {
    const isJpgOrJpeg = file.type === 'image/jpeg' || file.type === 'image/jpg';
    if (!isJpgOrJpeg) {
        message.error('You can only upload JPG or JPEG files!');
        return Upload.LIST_IGNORE;
    }
    return false;
};

// On change function
const onChange = ({fileList}) => {
    if (fileList.length > 1) {
        message.error('You can only upload one file!');
        fileList.splice(0, fileList.length - 1); // Remove all files except the last one
    }
};

export default NewFoodItem;