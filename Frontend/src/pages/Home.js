import React, {useEffect, useState} from 'react';
import {Col, message, Row, Typography} from 'antd';
import axios from "axios";
import RecipeCard from "../components/RecipeCard";

const {Title} = Typography;


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
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/recipe/`, {
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


    return (<div>
        <Title level={2} style={{textAlign: 'center'}}>My Dashboard</Title>
        <Row gutter={16}>
            {recipes.map((recipe, index) => (<Col key={index} span={8}>
                <RecipeCard recipe={recipe}/>
            </Col>))}
        </Row>
    </div>);
}