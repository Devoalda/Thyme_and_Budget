import React, {useEffect, useState} from 'react';
import {Col, message, Row, Typography} from 'antd';
import axios from "axios";
import LayoutComponent from '../components/Layout';
import FoodItemCard from "../components/FoodItemCard";

const {Title} = Typography;

export default function MyFoodItems() {
    const [foodItems, setFoodItems] = useState([]);

    // get data from local storage
    const token = localStorage.getItem('token');
    const refresh = localStorage.getItem('refresh');

    // get request to grab all food items of the current user
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/food/user_food_items/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setFoodItems(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                message.error('Failed to fetch food items. Please try again.');
            }
        };

        fetchData().then(r => '');
    }, []);

    return (<LayoutComponent>
            <div>
                <Title level={2} style={{textAlign: 'center'}}>My Food Items</Title>
                <Row gutter={16}>
                    {foodItems.map((foodItem, index) => (<Col key={index} span={8}>
                            <FoodItemCard foodItem={foodItem}/>
                        </Col>))}
                </Row>
            </div>
        </LayoutComponent>);
}