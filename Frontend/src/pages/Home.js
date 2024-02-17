import React, {useEffect, useState} from 'react';
import {Button, Col, message, Row, Spin, Typography} from 'antd';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import FoodItemCard from "../components/FoodItemCard";
import NoFoodItemCard from "../components/NoFoodItemCard";

const {Title} = Typography;

// Function to fetch food data
const fetchFoodData = async (setFood, setLoading, token) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/food/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (process.env.NODE_ENV === 'development') {
            console.log('Response:', response.data);
        }
        setFood(response.data);
    } catch (error) {
        if (process.env.NODE_ENV === 'development') {
            console.error('Error fetching data:', error);
        }
        if (error.response && error.response.status === 401) {
            message.error('Failed to fetch food items. Please try again.');
        }
    } finally {
        setLoading(false);
    }
};

// Function to render food items
const renderFoodItems = (food) => {
    return food.map((item, index) => (
        <Col key={index} span={8}>
            <FoodItemCard foodItem={item}/>
        </Col>
    ));
};

// Main function
export default function Home() {
    const [food, setFood] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // get data from local storage
    const token = localStorage.getItem('token');
    const refresh = localStorage.getItem('refresh');

    if (process.env.NODE_ENV === 'development') {
        console.log('Token:', token);
        console.log('Refresh:', refresh);
    }

    useEffect(() => {
        fetchFoodData(setFood, setLoading, token);
    }, []);

    return (
        <div>
            <Title level={2} style={{textAlign: 'center'}}>Thyme and Budget Food Items</Title>
            <Row gutter={16}>
                {loading ? (
                    <Spin />
                ) : food.length > 0 ? renderFoodItems(food) : (
                    <NoFoodItemCard />
                )}
            </Row>
        </div>
    );
}