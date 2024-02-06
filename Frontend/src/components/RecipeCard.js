import React from 'react';
import {Card, Space, Typography} from 'antd';
import PropTypes from 'prop-types';

const {Text} = Typography;

function RecipeCard({recipe}) {
    const defaultImageUrl = "https://via.placeholder.com/150";

    return (
        <Card
            title={recipe.title}
            cover={<img
                alt={recipe.title}
                src={recipe.image ? recipe.image : defaultImageUrl}
                style={{width: '100%', height: '150px', objectFit: 'cover'}}
            />}
            style={{
                backgroundColor: '#f8f9fa',
                color: '#343a40',
                padding: '20px',
                borderRadius: '10px',
                boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
            }}
        >
            <Space direction="vertical" size="small">
                <Text strong>Author: {recipe.author}</Text>
                <Text strong>Instructions: {recipe.instructions}</Text>
                <Text strong>Cooking Time: {recipe.cooking_time} minutes</Text>
                <Text strong>Budget: ${recipe.budget}</Text>
                <Text>Created At: {new Date(recipe.created_at).toLocaleString()}</Text>
                <Text>Updated At: {new Date(recipe.updated_at).toLocaleString()}</Text>
            </Space>
        </Card>
    );
}

RecipeCard.propTypes = {
    recipe: PropTypes.shape({
        title: PropTypes.string.isRequired,
        image: PropTypes.string,
        author: PropTypes.string.isRequired,
        instructions: PropTypes.string.isRequired,
        cooking_time: PropTypes.number.isRequired,
        budget: PropTypes.number.isRequired,
        created_at: PropTypes.string.isRequired,
        updated_at: PropTypes.string.isRequired,
    }).isRequired,
};

export default RecipeCard;