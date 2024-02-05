// pages/Error.js

import React from 'react';
import { Result, Button } from 'antd';
import { Link } from 'react-router-dom';

const Error = () => {
    return (
        <Result
            status="404"
            title="404 Not Found"
            subTitle="Sorry, the page you visited does not exist or you are not authorized to view it."
            extra={
                <Link to="/login">
                    <Button type="primary">Back to Login</Button>
                </Link>
            }
        />
    );
};

export default Error;
