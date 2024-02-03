import React from "react";
import { Breadcrumb } from 'antd';

export default function Header() {
    return (
        <Breadcrumb>
            <Breadcrumb.Item>Home</Breadcrumb.Item>
            <Breadcrumb.Item>
                <a href="">Recipes</a>
            </Breadcrumb.Item>
            <Breadcrumb.Item>
                <a href="">Nutrition Values</a>
            </Breadcrumb.Item>
            <Breadcrumb.Item>Get Meal Plan</Breadcrumb.Item>
        </Breadcrumb>
    );
}