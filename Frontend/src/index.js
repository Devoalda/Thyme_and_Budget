import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
// import layout
import Layout from "./components/Layout";
// import pages
import Registration from "./pages/Registration";
import Login from "./pages/Login";
import Home from "./pages/Home";

// default error page
import Error from "./pages/Error";

import Logout from "./pages/Logout";

// ...

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Router>
    <Routes>
        <Route path="/" element={<Registration/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/logout" element={<Logout/>}/>
        <Layout>
            <Route path="/home" element={<Home/>}/>
            //add routes below if want same layout
        </Layout>
        <Route path="*" element={<Error/>}/>
    </Routes>
</Router>);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
