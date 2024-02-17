import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Layout from './components/Layout';
import Registration from './pages/Registration';
import Login from './pages/Login';
import Home from './pages/Home';
import Error from './pages/Error';
import Logout from './pages/Logout';
import MyFoodItems from './pages/MyFoodItems';
import NewFoodItem from './pages/NewFoodItem';

function App() {
    return (<Router>
            <Routes>
                <Route path="/" element={<Registration/>}/>
                <Route path="/myfooditems" element={<MyFoodItems/>}/>
                <Route path="/newfooditem" element={<NewFoodItem/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/logout" element={<Logout/>}/>
                <Route
                    path="/home"
                    element={<Layout>
                        <Home/>
                    </Layout>}
                />
                <Route path="*" element={<Error/>}/>
            </Routes>
        </Router>);
}

export default App;