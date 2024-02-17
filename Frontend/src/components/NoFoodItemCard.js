import React from 'react';
import {Button, Card} from 'antd';
import {useNavigate} from 'react-router-dom';

const cardStyle = {
    backgroundColor: '#f8f9fa',
    color: '#343a40',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
    marginBottom: '20px',
    textAlign: 'center',
};

const buttonStyle = {
    backgroundColor: '#007bff',
    borderColor: '#007bff',
    color: '#fff',
    width: '100%',
    marginTop: '20px',
};

function NoFoodItemCard() {
    const navigate = useNavigate();

    return (
        <Card style={cardStyle}>
            <p>No food items found. Would you like to add one for donation?</p>
            <Button type="primary" style={buttonStyle} onClick={() => navigate('/newfooditem')}>Add Food Item</Button>
        </Card>
    );
}

export default NoFoodItemCard;