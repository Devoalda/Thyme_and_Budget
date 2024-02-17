import React from 'react';
import {Menu} from 'antd';
import {Link, useLocation} from 'react-router-dom';

const {Item} = Menu;

export default function Header() {
    const location = useLocation();
    const currentPath = location.pathname;

    return (
        <Menu mode="horizontal" selectedKeys={[currentPath]}>
            <Item key="/home">
                <Link to="/home">Home</Link>
            </Item>
            {/*<Item key="/recipes">*/}
            {/*    <Link to="/recipes">Recipes</Link>*/}
            {/*</Item>*/}
            {/*<Item key="/nutrition">*/}
            {/*    <Link to="/nutrition">Nutrition Values</Link>*/}
            {/*</Item>*/}
            {/*<Item key="/mealplan">*/}
            {/*    <Link to="/mealplan">Get Meal Plan</Link>*/}
            {/*</Item>*/}
            <Item key="/myfooditems">
                <Link to="/myfooditems">My Food Items</Link>
            </Item>
            <Item key="/newfooditem">
                <Link to="/newfooditem">New Food Item</Link>
            </Item>
            <Item key="/logout">
                <Link to="/logout">Logout</Link>
            </Item>
        </Menu>
    );
}