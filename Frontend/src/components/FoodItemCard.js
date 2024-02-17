import React from 'react';
import {Card, Space, Typography, Button} from 'antd';
import PropTypes from 'prop-types';

const {Text} = Typography;

function FoodItemCard({foodItem}) {
    const defaultImageUrl = "https://via.placeholder.com/150";

    return (
        <Card
            title={foodItem.name}
            cover={<img
                alt={foodItem.name}
                src={foodItem.image ? foodItem.image : defaultImageUrl}
                style={{width: '100%', height: '150px', objectFit: 'cover'}}
            />}
            style={{
                backgroundColor: '#f8f9fa',
                color: '#343a40',
                padding: '20px',
                borderRadius: '10px',
                boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
                marginBottom: '20px',
            }}
        >
            <Space direction="vertical" size="small">
                <Text strong>Expiry Date: {new Date(foodItem.expiry_date).toLocaleString()}</Text>
                <Text strong>Location: {foodItem.location}</Text>
                <Text strong>Quantity: {foodItem.quantity}</Text>
                <Button type="primary" style={{marginTop: '10px'}}>Add to Collection</Button>
            </Space>
        </Card>
    );
}

FoodItemCard.propTypes = {
    foodItem: PropTypes.shape({
        name: PropTypes.string.isRequired,
        image: PropTypes.string,
        expiry_date: PropTypes.string.isRequired,
        location: PropTypes.string.isRequired,
        quantity: PropTypes.number.isRequired,
    }).isRequired,
};

export default FoodItemCard;