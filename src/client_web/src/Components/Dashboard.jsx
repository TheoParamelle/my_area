import React from "react";
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';


const Dashboard = ({ username }) => {
    return (

        <div>
            <br/>
            <br/>
            <br/>
            <br/>
            <h1>Dashboard</h1>
            {/* <h4>What you can do .. </h4> */}
            <br/>
            <Link to="/addServices">
                <Button variant="primary">
                    Services connection
                </Button>
            </Link>
            <br/>
            <br/>
            <br/>
            <br/>
            <Link to="/addArea">
                <Button variant="primary">
                    Add an Area
                </Button>
            </Link>
            <br/>
            <br/>
            <br/>
            <br/>
            <Link to="/setTexts">
                <Button variant="primary">
                    Customisation
                </Button>
            </Link>
            <br/>
            {/* usename = {username} */}
        </div>
    );
}

export default Dashboard ;
