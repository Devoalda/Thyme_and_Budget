import React, {useEffect, useState} from 'react';
import {Col, message, Row, Typography} from 'antd';
import axios from "axios";
import LayoutComponent from '../components/Layout';
import RecipeCard from "../components/RecipeCard";

const {Title} = Typography;

export default function MyRecipes() {
    const [recipes, setRecipes] = useState([]);

    // get data from local storage
    const token = localStorage.getItem('token');
    const refresh = localStorage.getItem('refresh');

    // get request to grab all recipes of the current user
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/recipe/user_recipes/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setRecipes(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                message.error('Failed to fetch recipes. Please try again.');
            }
        };

        fetchData().then(r => '');
    }, []);

    return (<LayoutComponent>
            <div>
                <Title level={2} style={{textAlign: 'center'}}>My Recipes</Title>
                <Row gutter={16}>
                    {recipes.map((recipe, index) => (<Col key={index} span={8}>
                            <RecipeCard recipe={recipe}/>
                        </Col>))}
                </Row>
            </div>
        </LayoutComponent>);
}