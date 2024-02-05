import React from 'react';
import { Menu } from 'antd';
import { Link } from 'react-router-dom';

const { Item } = Menu;

export default function Header() {
    return (
        <Menu mode="horizontal">
            <Item key="home">
                <Link to="/">Home</Link>
            </Item>
            <Item key="recipes">
                <Link to="/recipes">Recipes</Link>
            </Item>
            <Item key="nutrition">
                <Link to="/nutrition">Nutrition Values</Link>
            </Item>
            <Item key="mealplan">
                <Link to="/mealplan">Get Meal Plan</Link>
            </Item>
            <Item key="logout">
                <Link to="/logout">Logout</Link>
            </Item>
        </Menu>
    );
}