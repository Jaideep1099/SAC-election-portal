import './style/login.css';

import axios from 'axios';
import React, { useState } from 'react';
import { url } from './config' ;

function Login(props) {

    const { setLoggedIn, setUser, loadCandidates } = props;
    const [formData, setFormData] = useState({ 'uname': '', 'pwd': '' });

    const [error, setError] = useState("");

    function handleChange(event) {
        var elementName = event.target.name;
        var value = event.target.value;

        setFormData((prevValue) => {
            if (elementName === "uname") {
                return {
                    ...prevValue,
                    'uname': value
                }
            }
            else if (elementName === "pwd") {
                return {
                    ...prevValue,
                    pwd: value
                }
            }
        })
        console.log(formData);
    }

    function handleClick() {
        setError("");
        axios.post(url+"/login", formData).then(res => {
            console.log(res);
            setUser({ uname: formData['uname'], token: res.data.token });
            loadCandidates()
            setLoggedIn(true);
        }).catch(err => {
            console.log(err);
            setError("Login Failed");
        })
    }

    return (
        <div className="back">
            <div className="center">
                <h1>Login</h1>
                <form method="post">
                    <div className="txt_field">
                        <input type="text" name="uname" onChange={handleChange} required />
                        <span></span>
                        <label>Username</label>
                    </div>

                    <div className="txt_field">
                        <input type="password" name="pwd" onChange={handleChange} required />
                        <span></span>
                        <label>Password</label>
                    </div>
                    {/* <div className="pass">Forgot Password?</div> */}
                    <input type="button" value="Login" onClick={handleClick} />
                    <div className="signup_link">
                        {/* Not a member?<a href="#">Signup</a> */}
                    </div>
                    <p>{error}</p>
                </form>
            </div>
        </div>

    );
}

export default Login;