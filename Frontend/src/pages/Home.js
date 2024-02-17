import React, {useEffect, useState} from 'react';
import {Col, message, Row, Typography} from 'antd';
import axios from "axios";
import FoodItemCard from "../components/FoodItemCard";

const {Title} = Typography;


export default function Home() {
    const [food, setFood] = useState([]);

    // get data from local storage
    const token = localStorage.getItem('token');
    const refresh = localStorage.getItem('refresh');
    console.log('Token:', token);
    console.log('Refresh:', refresh);


    // get request to grab all food
    useEffect(() => {
        const fetchData = async () => {
            try {
                // Make a GET request to the specified endpoint
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/food/`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                console.log('Response:', response.data);
                // Update the recipes state with the data from the response
                setFood(response.data);

            } catch (error) {
                console.error('Error fetching data:', error);
                // Handle the error, e.g., show an error message to the user
                message.error('Failed to fetch recipes. Please try again.');
            }
        };

        // Call the fetchData function when the component mounts
        fetchData().then(r => '');
    }, []);


    return (<div>
        <Title level={2} style={{textAlign: 'center'}}>Thyme and Budget Food Items</Title>
        <Row gutter={16}>
            {food.map((item, index) => (<Col key={index} span={8}>
                <FoodItemCard foodItem={item}/>
            </Col>))}
        </Row>
    </div>);
}