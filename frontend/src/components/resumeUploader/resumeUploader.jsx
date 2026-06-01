import React from "react";
import { useState } from "react";
import axios from "axios";

function ResumeUploader({ setAnalysis, setJobs }) {
    const [file, setFile] = useState(null);
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [response, setResponse] = useState(null);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }
        const formData = new FormData();
        formData.append("resume", file);

        try {
            const data = await axios.post(`${BACKEND_URL}/api/upload`, formData);

            if (data.status === 200) {
                alert("File uploaded successfully!");
                setResponse(data.data);
                setAnalysis(data.data.analysis);
                //console.log(data.data.analysis);
                setJobs(data.data.job_listings);
            }
            else {
                alert("Failed to upload file.");
            }
        }
        catch (error) {
            alert("An error occurred while uploading the file.");
        }
    }
    return (
        <>
            <h1>Upload Your Resume in PDF Format</h1>
            <div className="resume-uploader">
                <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
                <button onClick={handleUpload}>Upload</button>
            </div>
            {response ? (
                <p>
                    Analysis Result: We completed the resume analysis.
                    To view the analysis and job listings, switch tabs.
                </p>
            ) : (
                <p>
                    No response yet. Please upload a resume to see the
                    analysis and job listings.
                </p>
            )}
        </>
    )
}

export default ResumeUploader;