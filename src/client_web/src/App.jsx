import {
    Routes,
    Route,
  } from "react-router-dom";
import Login from "./Components/Login"
import Dashboard from "./Components/Dashboard"
import NewAccount from "./Components/newAccount";
import Home from "./Components/Home";
import AddServices from "./Components/Services/AddServices";
import AddArea from "./Components/Services/AddAera";
import SetTexts from "./Components/Services/setTexts";
import background from "./img/degrade.jpg"
import './App.css';
import { useState, useEffect } from "react";

function App() {
    const [username, setUser] = useState('')

    useEffect(() => {
        setUser(localStorage.getItem("username"))
      }, []);

    return (
        <div
        className="dashboard"
        style={{
        backgroundImage: `url(${background})`,
        height:'100vh',
        // marginTop:'-70px',
        fontSize:'20px',
        backgroundSize: 'cover',
        // backgroundRepeat: 'no-repeat',
      }}>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <div class="container-fluid">
                    <a class="navbar-brand" href="/">AREA</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                        <a class="nav-link" href="/login">Profil</a>
                        </li>
                        <li class="nav-item">
                        <a class="nav-link" href="/Dashboard">Dashboard</a>
                        </li>
                    </ul>
                    </div>
                </div>
            </nav>
            {/* <nav>
            <ul>
                <li>
                <Link to="/">Home</Link>
                </li>
                <li>
                <Link to="/login">Login</Link>
                </li>
                <li>
                <Link to="/Dashboard">Dashboard</Link>
                </li>
            </ul>
            </nav> */}
            <Routes>
                <Route path="" element={<Home/>}/>
                <Route path="login" element={<Login setUser={setUser} username={username}/>}/>
                <Route path="Dashboard" element={<Dashboard username={username}/>}/>
                <Route path="createNewAccount" element={<NewAccount/>}/>
                <Route path="addServices" element={<AddServices username={username}/>}/>
                <Route path="addArea" element={<AddArea username={username}/>}/>
                <Route path="setTexts" element={<SetTexts username={username}/>}/>
            </Routes>
        </div>
    );
}

export default App;
