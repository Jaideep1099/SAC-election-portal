import axios from 'axios';
import React, { useState } from 'react';
import url from './config' ;

function VotingPage(props) {
    const { candidates, user, setLoggedIn } = props;

    const [selected, setSelected] = useState({});

    const onChange = event => {
        console.log(event.target);

        const key = event.target.name
        const val = event.target.value

        setSelected(prev => {
            let newSelected = { ...prev };
            newSelected[key] = val;
            return newSelected;
        });
        console.log(selected);
    };

    function logout() {
        axios.post(url+"/logout", user).then((res) => {
            setLoggedIn(false)
        }).catch((err) => {
            console.log(err);
        })
    }

    const castVote = () => {
        if (Object.keys(selected).length === Object.keys(candidates).length) {

            const data = { ...selected, ...user }

            axios.post(url+"/castvote", data).then((res) => {
                console.log(res);
                alert("Your vote has been saved. You will be now logged out")
                logout();
            }).catch((err) => {
                alert(err.response.data.error)
            })
        } else {
            alert('Select your choices for all positions')
        }
    }

    return (
        <div>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                        <div class="navbar-nav">
                            <button class="btn btn-outline-primary" onClick={logout}> Logout </button>
                        </div>
                    </div>
                </div>
            </nav>
            {Object.keys(candidates).map((pos, ind) => (
                <div key={ind}>
                    <h3>{pos}</h3>
                    <div class="card" style={{ width: '18rem' }}>
                        <ul class="list-group list-group-flush">
                            {candidates[pos].map((cand, ind) => (
                                <div key={ind}>
                                    <li class="list-group-item">
                                        <input type="radio" id={cand['rollno']} name={pos} value={cand['rollno']} onChange={onChange} />
                                        <label for={cand['rollno']}>{cand['name'] + ' - [ ' + cand['program'] + ' ' + cand['dept'] + ' ]'}</label>
                                    </li>
                                </div>
                            ))}
                        </ul>
                    </div>
                </div>
            ))}
            <div style={{ padding: '10px' }}>
                <button class="btn btn-outline-primary" onClick={castVote}>Vote</button>
            </div>
        </div>
    );
}


export default VotingPage;