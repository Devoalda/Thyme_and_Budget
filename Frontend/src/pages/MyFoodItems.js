import React, {useEffect, useState} from 'react';
import {Col, message, Row, Spin, Typography} from 'antd';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import LayoutComponent from '../components/Layout';
import FoodItemCard from "../components/FoodItemCard";
import NoFoodItemCard from "../components/NoFoodItemCard";

const {Title} = Typography;

// Function to fetch food data
const fetchFoodData = async (setFoodItems, setLoading, token) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/food/user_food_items/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        setFoodItems(response.data);
    } catch (error) {
        if (process.env.NODE_ENV === 'development') {
            console.error('Error fetching data:', error);
        }
        message.error('Failed to fetch food items. Please try again.');
    } finally {
        setLoading(false);
    }
};

// Function to render food items
const renderFoodItems = (foodItems) => {
    return foodItems.map((foodItem, index) => (<Col key={index} span={8}>
        <FoodItemCard foodItem={foodItem}/>
    </Col>));
};

// Main function
export default function MyFoodItems() {
    const [foodItems, setFoodItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // get data from local storage
    const token = localStorage.getItem('token');

    useEffect(() => {
        fetchFoodData(setFoodItems, setLoading, token);
    }, []);

    return (<LayoutComponent>
        <div>
            <Title level={2} style={{textAlign: 'center'}}>My Food Items</Title>
            <Row gutter={16}>
                {loading ? (<Spin/>) : foodItems.length > 0 ? renderFoodItems(foodItems) : (<NoFoodItemCard/>)}
            </Row>
        </div>
    </LayoutComponent>);
}