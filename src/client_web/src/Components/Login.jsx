import React from "react";
import { useState } from "react";
import {Link } from "react-router-dom";
// import { Dashboard } from "./Dashboard";


const Login = ({setUser, username}) => {

    const [name, setName] = useState(username)
    const [password, setPass] = useState('')
    const [status, setStatus] = useState('')
    const [color, setColor] = useState('')

    function verifyCount() {
        console.log("send to back");
        console.log(name, password)
        fetch('login',
        {
            'method':'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({"username": name, "password": password})
        })
        .then(res => res.json())
        .then(data => {
            if (data["username"] === true && data["password"] === true) {
                setStatus("SUCCESS !")
                setColor("h4 text-success")
                setUser(name)
                localStorage.setItem("username", name)
            }
            else if (data["username"] === false) {
                setStatus("User not register, create a new account")
                setColor("h4 text-warning")
            }
            else {
                setStatus("Password not good")
                setColor("h4 text-warning")
            }
        })
    }

    return (
        <div className="login">
            <h1>Login</h1>
            <div>
                <input 
                placeholder="Username"
                onChange={event => setName(event.target.value)}
                />
            </div>
            <div>
                <input 
                placeholder="Password"
                onChange={event => setPass(event.target.value)}
                />
            </div>
            <br/>
            <button type="button" class="btn btn-primary"onClick={() => verifyCount()}>Login</button>
            <br/>
            <br/>
            <Link to="/createNewAccount">
                <button type="button" class="btn btn-secondary">New Acccount</button>
            </Link>

            <div>
                <br/>
                <br/>
                <br/>
            <p class={color}>{status}</p>
            </div>
        </div>
    );
}

export default Login