import axios from 'axios';

import React, { useState } from 'react';



function CandidateUploader(props) {

    const { user } = props;
    const [selectedFile, setSelectedFile] = useState(null)

    const [status, setStatus] = useState("");

    // On file select (from the pop up)
    const onFileChange = event => {
        // Update the state
        setSelectedFile(event.target.files[0])
    };

    // On file upload (click the upload button)
    const onFileUpload = () => {

        setStatus("");

        if(selectedFile===null) {
            setStatus("Please select a file");
            return;
        }

        // Create an object of formData
        const formData = new FormData();

        // Update the formData object
        formData.append(
            "file",
            selectedFile,
            selectedFile.name,
        );

        formData.append('token',user.token);

        // Details of the uploaded file
        console.log(selectedFile);

        // Request made to the backend api
        // Send formData object
        axios.post("http://localhost:1234/candidateuploader", formData).then((res) => {
            console.log(res);
            setStatus("Candidate list updated successfully !")
        }).catch((err) => {
            console.log(err);
            setStatus("File upload failed !")
        })

    };

    return (
        <div>
            <h1>
                Upload CandidateList
            </h1>
            <div>
                <input class="form-label" type="file" onChange={onFileChange} accept=".xls, .xlsx" />
                <button class="btn btn-primary btn-sm" onClick={onFileUpload}>
                    Upload!
                </button>
                <p>{status}</p>
            </div>
        </div>
    );
}


export default CandidateUploader;