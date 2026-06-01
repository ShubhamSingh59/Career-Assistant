import react, { useState } from "react";
import axios from "axios";

function ResumeAnalysis({ response }) {
    if (!response) {
        return <p>No analysis data available. Please upload a resume to see the analysis.</p>;
    }
    return (
        <div>
            <section className="card">
                <h2>Over Impression</h2>
                <p>{response.overall_impression || "No data available"}</p>
            </section>
            <section className="card">
                <h2>Core Strengths</h2>
                <ul>
                    {
                        response.core_strengths.map(
                            (strength, index) => (<li key={index}>
                                {strength}
                            </li>
                            )
                        )
                    }
                </ul>
            </section>
            <section className="card">
                <h2>Areas for Improvement</h2>
                <ul>
                    {
                        response.areas_for_improvement.map(
                            (area, index) => (<li key={index}>
                                {area}
                            </li>
                            )
                        )
                    }
                </ul>
            </section>
            <section className="card">
                <h2>Actionable Steps</h2>
                <ul>
                    {
                        response.actionable_steps.map(
                            (step, index) => (<li key={index}>
                                {step}
                            </li>
                            )
                        )
                    }
                </ul>
            </section>
            <section className="card">
                <h2>ATS Readiness</h2>
                <p>{response.ats_readiness || "No data available"}</p>
            </section>
             <section className="card">
                <h2>Predicted Job Roles</h2>
                <ul>
                    {
                        response.predicted_job_titles.map(
                            (role, index) => (<span key={index}>
                                {role}
                            </span>
                            )
                        )
                    }
                </ul>
            </section>
        </div>
    )
}

export default ResumeAnalysis;