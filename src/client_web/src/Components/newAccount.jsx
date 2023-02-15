import React from "react";
import {Link } from "react-router-dom";
import { useState } from "react";

const NewAccount = () => {

    const [name, setName] = useState('')
    const [password, setPass] = useState('')
    const [status, setStatus] = useState('')
    const [color, setColor] = useState('')

    function verif_args() {
        if (name === "" || password === "") {
            setStatus("Empty fields !!!")
            setColor("h4 text-warning")
            return false
        }
        return true
    }

    function createNewAccount() {
        if (verif_args() === false)
            return;
        fetch('login', 
        {
            'method':'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({"username": name, "password": password, "newAccount": true})
        })
        .then(res => res.json())
        .then(data => {
            if (data["username"] === true) {
                setStatus("username already exist, login with your account")
                setColor("h4 text-warning")
            } else if (data["username"] === false) {
                setStatus("Your acount has been created !")
                setColor("h4 text-success")
            }
        })
    }

    return (
        <div className="login">
            <h1>New Account</h1>
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
            <button type="button" class="btn btn-primary" onClick={() => createNewAccount()}>Create new account</button>
            <br/>
            <br/>
            <Link to="/login">
                <button type="button" class="btn btn-secondary">Return to login</button>
            </Link>
            <br/>
            <div>
                <br/>
                <br/>
                <br/>
            <p class={color}>{status}</p>
            </div>
        </div>
    );
}

export default NewAccount;