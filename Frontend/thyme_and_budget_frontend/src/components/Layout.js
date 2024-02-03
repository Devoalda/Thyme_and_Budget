// components/Layout.js

import React from 'react';
import { Layout } from 'antd';
import Header from './Header';

const { Content, Footer } = Layout;

const layoutStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
};

export default function LayoutComponent({ children }) {
    return (
        <Layout style={layoutStyle}>
            <Header />
            <Content style={{ padding: '0 50px' }}>
                <div className="site-layout-content">{children}</div>
            </Content>
            <Footer style={{ textAlign: 'center' }}>Thyme & Budget ©2024 Created by Team 15</Footer>
        </Layout>
    );
}