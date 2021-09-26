import axios from 'axios';
import React, { useState } from 'react';

function VotingPage(props) {
    const { candidates, user, setLoggedIn } = props;
    const [selected, setSelected] = useState({ 'gensec': null, 'sportsec': null });

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
        axios.post("http://localhost:1234/logout", user).then((res) => {
            setLoggedIn(false)
        }).catch((err) => {
            console.log(err);
        })
    }

    const castVote = () => {
        if (selected['gensec'] !== null && selected['sportsec'] !== null) {

            const data = { ...selected, ...user }

            axios.post("http://localhost:1234/castvote", data).then((res) => {
                console.log(res);
                alert("Your vote has been saved. You will be now logged out")
                logout();
            }).catch((err) => {
                alert(err.response.data.error)
            })
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
            <div>
                <h3> General Secretary </h3>
                <div class="card" style={{ width: '18rem' }}>
                    <ul class="list-group list-group-flush">

                        {candidates['gensec'].map((cand, ind) => (
                            <div key={ind}>
                                <li class="list-group-item"><input type="radio" id={cand['rollno']} name='gensec' value={cand['rollno']} onChange={onChange} />
                                    <label for={cand['rollno']}>{cand['name'] + ' - [ ' + cand['program'] + ' ' + cand['dept'] + ' ]'}</label>
                                </li>
                            </div>
                        ))}
                    </ul>
                </div>
            </div>
            <div>
                <h3> Sports Secretary </h3>
                <div class="card" style={{ width: '18rem' }}>
                    <ul class="list-group list-group-flush">
                        {candidates['sportsec'].map((cand, ind) => (
                            <div key={ind}>
                                <li class="list-group-item">
                                    <input type="radio" id={cand['rollno']} name='sportsec' value={cand['rollno']} onChange={onChange} />
                                    <label for={cand['rollno']}>{cand['name'] + ' - [ ' + cand['program'] + ' ' + cand['dept'] + ' ]'}</label>
                                </li>
                            </div>
                        ))}
                    </ul>
                </div>
            </div>
            <div style={{ padding: '10px' }}>
                <button class="btn btn-outline-primary" onClick={castVote}>Vote</button>
            </div>
        </div>
    );
}


export default VotingPage;