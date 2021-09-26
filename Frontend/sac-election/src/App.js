import axios from "axios";
import Login from "./login";
import React, { useState } from 'react';
import AdminPage from "./adminPage";
import VotingPage from "./votingPage";

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser] = useState({ uname: '', token: '' })
  const [candidates, setCandidates] = useState(null)

  const loadCandidates = () => {
    axios.post("http://localhost:1234/fetchcandidates").then((res) => {
      console.log(res);
      setCandidates({ ...res.data })
    }).catch((err) => {
      console.log(err);
    })
  }
  return (
    <>
      {!loggedIn ? <Login setLoggedIn={setLoggedIn} setUser={setUser} loadCandidates={loadCandidates} /> : null}
      {loggedIn && user.uname === 'admin' ? <AdminPage user={user} setLoggedIn={setLoggedIn}/> : null}
      {loggedIn && user.uname !== 'admin' && candidates !== null ? <VotingPage candidates={candidates} user={user} setLoggedIn={setLoggedIn} /> : null}
    </>
  );
}

export default App;
