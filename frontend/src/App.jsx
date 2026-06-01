import { useState } from 'react'
import './App.css'
import ResumeUploader from './components/resumeUploader/resumeUploader';
import ResumeAnalysis from './components/resumeAnalysis/analysis';
import JobList from './components/jobListing/jobList';

function App() {
  const[analysis, setAnalysis] = useState(null);
  const [jobs, setJobs] = useState(null);
  const [activeTab, setActiveTab] = useState("upload");
  return (
    <>
      <h1>Welcome to the Frontend!</h1>
      <div className="tabs">
        <button onClick={() => setActiveTab("upload")} >Resume Upload</button>
        <button onClick={() => setActiveTab("analysis")} disabled={!analysis}>Resume Analysis</button>
        <button onClick={() => setActiveTab("jobs")} disabled={!jobs}>Job Listings</button>
      </div>

      {activeTab === "upload" && <ResumeUploader setAnalysis={setAnalysis} setJobs={setJobs} />}
      {activeTab === "analysis" && <ResumeAnalysis response={analysis} />}
      {activeTab === "jobs" && <JobList jobs={jobs} />}
    </>
  )
}

export default App
