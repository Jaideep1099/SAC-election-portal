import React, { useEffect, useState } from 'react';
import VotersUploader from './votersUploader';
import CandidateUploader from './candidateUploader';
import axios from 'axios';
import url from './config';

function AdminPage(props) {
    const { user, setLoggedIn } = props;
    const [section, setSection] = useState('voters');
    const [result, setResult] = useState(null);
    const [voting, setVoting] = useState(false);

    useEffect(() => {
        fetchVote();
    }, [])

    function logout() {
        axios.post(url + "/logout", user).then((res) => {
            setLoggedIn(false)
        }).catch((err) => {
            console.log(err);
        })
    }

    function fetchResults() {
        axios.post(url + "/fetchresults", user).then((res) => {
            setResult(res.data)
        }).catch((err) => {
            console.log(err);
        })
    }

    function fetchVote() {
        axios.post(url + "/getvotestatus", user).then((res) => {
            setVoting(res.data.voting_started);
            console.log(res.data.voting_started);
        }).catch((err) => {
            console.log(err);
        })
    }

    function deleteVoters() {
        axios.post(url + "/deletevoters", user).then((res) => {
            alert("Voters deleted successfully");
        }).catch((err) => {
            alert(err.response.data.error);
            console.log(err);
        })
    }

    function deleteCandidates() {
        axios.post(url + "/deletecandidates", user).then((res) => {
            alert("Candidates deleted");
        }).catch((err) => {
            alert(err.response.data.error);
            console.log(err);
        })
    }

    function toggleVote() {
        axios.post(url + "/togglevoting", user).then((res) => {
            fetchVote();
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
                            <button class="btn btn-outline-primary" onClick={toggleVote}> Toggle Voting </button>
                            {section === 'voters' ? <button class="btn btn-outline-primary" onClick={deleteVoters}> Delete Voters </button> : <button class="btn btn-outline-primary" onClick={deleteCandidates}> Delete Candidates </button>}
                        </div>
                    </div>
                </div>
            </nav>
            {section === 'voters' ? <VotersUploader user={user} /> : <CandidateUploader user={user} />}
            <br /><br />
            <p class="alert alert-info">Voting Status: {voting === true ? 'Started' : 'Closed'}</p>
            <br /><br />
            <button class="btn btn-primary btn-sm" onClick={fetchResults}> Show Results </button>
            {result === null ? null
                :
                Object.keys(result).map((pos, ind) => (
                    <div key={ind}>
                        <h3>{pos}</h3>
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
                                {result[pos].map((cand, ind) =>
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
                    </div>
                ))
            }
        </div >
    );
}

export default AdminPage;