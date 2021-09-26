import React, { useState } from 'react';
import VotersUploader from './votersUploader';
import CandidateUploader from './candidateUploader';
import axios from 'axios';

function AdminPage(props) {
    const { user, setLoggedIn } = props;
    const [section, setSection] = useState('voters');
    const [result, setResult] = useState(null);

    function logout() {
        axios.post("http://localhost:1234/logout", user).then((res) => {
            setLoggedIn(false)
        }).catch((err) => {
            console.log(err);
        })
    }

    function fetchResults() {
        axios.post("http://localhost:1234/fetchresults", user).then((res) => {
            setResult(res.data)
        }).catch((err) => {
            console.log(err);
        })
    }

    function onClick() {
        setSection(prevValue => {
            if (prevValue === 'voters') {
                return 'candidate';
            }
            else
                return 'voters';
        })

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
                            <button class="btn btn-outline-primary" onClick={onClick}>{section === 'voters' ? "Candidate Upload" : "Voter Upload"}</button>
                        </div>
                    </div>
                </div>
            </nav>
            {section === 'voters' ? <VotersUploader user={user} /> : <CandidateUploader user={user} />}
            <br /><br />
            <button class="btn btn-primary btn-sm" onClick={fetchResults}> Show Results </button>
            {result === null ? null
                :
                <div>
                    <h3> General Secretary </h3>
                    <table class="table table-sm">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">Rank</th>
                                <th scope="col">Name</th>
                                <th scope="col">Roll No</th>
                                <th scope="col">Department</th>
                                <th scope="col">Program</th>
                                <th scope="col">Votes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {result['gensec'].map((cand, ind) =>
                                <tr key={ind}>
                                    <th scope="row">{ind + 1}</th>
                                    <td>{cand['name']}</td>
                                    <td>{cand['rollno']}</td>
                                    <td>{cand['dept']}</td>
                                    <td>{cand['program']}</td>
                                    <td>{cand['votes']}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                    <h3> Sports Secretary </h3>
                    <table class="table table-sm">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">Rank</th>
                                <th scope="col">Name</th>
                                <th scope="col">Roll No</th>
                                <th scope="col">Department</th>
                                <th scope="col">Program</th>
                                <th scope="col">Votes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {result['sportsec'].map((cand, ind) =>

                                <tr key={ind}>
                                    <th scope="row">{ind + 1}</th>
                                    <td>{cand['name']}</td>
                                    <td>{cand['rollno']}</td>
                                    <td>{cand['dept']}</td>
                                    <td>{cand['program']}</td>
                                    <td>{cand['votes']}</td>
                                </tr>

                            )}
                        </tbody>
                    </table>
                </div>}


        </div>
    );
}


export default AdminPage;