import React from 'react';
import {Card, Space, Typography, Button} from 'antd';
import PropTypes from 'prop-types';

const {Text} = Typography;

// Styles
const cardStyle = {
    backgroundColor: '#f8f9fa',
    color: '#343a40',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
    marginBottom: '20px',
};

const imgStyle = {width: '100%', height: '150px', objectFit: 'cover'};

// Function to render image
const renderImage = (foodItem, defaultImageUrl) => (
    <img
        alt={foodItem.name}
        src={foodItem.image ? foodItem.image : defaultImageUrl}
        style={imgStyle}
    />
);

// Function to render text fields
const renderTextFields = (foodItem) => (
    <Space direction="vertical" size="small">
        <Text strong>Expiry Date: {new Date(foodItem.expiry_date).toLocaleString()}</Text>
        <Text strong>Location: {foodItem.location}</Text>
        <Text strong>Quantity: {foodItem.quantity}</Text>
    </Space>
);

// Main function
function FoodItemCard({foodItem}) {
    const defaultImageUrl = "https://via.placeholder.com/150";

    return (
        <Card
            title={foodItem.name}
            cover={renderImage(foodItem, defaultImageUrl)}
            style={cardStyle}
            actions={[
                <Button type="primary" style={{width: '100%'}}>Add to Collection</Button>
            ]}
        >
            {renderTextFields(foodItem)}
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