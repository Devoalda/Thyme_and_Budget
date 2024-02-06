import React, {useState, useEffect} from 'react';
import {Card, Row, Col, Typography, Space, message} from 'antd';
import axios from "axios";

const {Title, Text} = Typography;

export default function Home() {
    const [recipes, setRecipes] = useState([]);

    // get data from local storage
    const token = localStorage.getItem('token');
    const refresh = localStorage.getItem('refresh');
    console.log('Token:', token);
    console.log('Refresh:', refresh);


    // get request to grab all recipes
    useEffect(() => {
        const fetchData = async () => {
            try {
                // Make a GET request to the specified endpoint
                const response = await axios.get('http://127.0.0.1:8000/recipe/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                console.log('Response:', response.data);
                // Update the recipes state with the data from the response
                setRecipes(response.data);

            } catch (error) {
                console.error('Error fetching data:', error);
                // Handle the error, e.g., show an error message to the user
                message.error('Failed to fetch recipes. Please try again.');
            }
        };

        // Call the fetchData function when the component mounts
        fetchData().then(r => '');
    }, []);


    return (
        <div>
            <Title level={2} style={{textAlign:'center'}}>My Dashboard</Title>
            <Row gutter={16}>
                {recipes.map((recipe, index) => (
                    <Col key={index} span={8}>
                        <Card
                            title={recipes.title}
                            cover={<img alt={recipe.title} src={recipes.image}/>}
                        >
                            <Space direction="vertical" size="small">
                                <Text strong>Author: {recipe.author}</Text>
                                <Text strong>Instructions: {recipes.instructions}</Text>
                                <Text strong>Cooking Time: {recipes.cooking_time} minutes</Text>
                                <Text strong>Budget: ${recipes.budget}</Text>
                                <Text>Created At: {new Date(recipes.created_at).toLocaleString()}</Text>
                                <Text>Updated At: {new Date(recipes.updated_at).toLocaleString()}</Text>
                            </Space>
                        </Card>
                    </Col>
                ))}
            </Row>
        </div>
    );
}