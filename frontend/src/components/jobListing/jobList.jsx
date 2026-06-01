import React, { useState } from "react";
import axios from "axios";

function JobList({ jobs }) {
    // State to hold fetched overviews: { "CompanyName": "Overview text..." }
    const [overviews, setOverviews] = useState({});
    // State to track loading status per company: { "CompanyName": true/false }
    const [loading, setLoading] = useState({});

    if (!jobs || jobs.length === 0) {
        return (
            <p>
                No job listings available. Please upload a resume first.
            </p>
        );
    }

    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    const handleSearchOverview = async (companyName) => {
        if (!companyName) {
            console.warn("Company name not available for research.");
            return;
        }

        // Set loading to true for this specific company
        setLoading((prev) => ({ ...prev, [companyName]: true }));

        try {
            const companySummary = await axios.get(
                `${BACKEND_URL}/api/company-research`,
                { params: { company_name: companyName } }
            );

            if (companySummary.status === 200) {
                // Store the result in state mapped to the company name
                setOverviews((prev) => ({
                    ...prev,
                    [companyName]: companySummary.data.company_summary,
                }));
            } else {
                setOverviews((prev) => ({
                    ...prev,
                    [companyName]: "Failed to fetch company overview.",
                }));
            }
        } catch (error) {
            console.error("Error fetching company overview:", error);
            setOverviews((prev) => ({
                ...prev,
                [companyName]: "Error occurred while fetching company overview.",
            }));
        } finally {
            // Remove loading state once the request completes
            setLoading((prev) => ({ ...prev, [companyName]: false }));
        }
    };

    return (
        <div>
            <h2>Recommended Job Listings</h2>

            {jobs.map((job, index) => (
                <section className="card" key={index}>
                    <h3>{job.job_title || "No title available"}</h3>

                    <p>
                        <strong>Company:</strong> {job.company || "Not mentioned"}
                    </p>

                    <p>
                        <strong>Location:</strong> {job.location || "Not mentioned"}
                    </p>

                    {job.money && job.money !== "0" ? (
                        <p>
                            <strong>Salary:</strong> {job.money}
                        </p>
                    ) : null}

                    {job.description && <p>{job.description}</p>}

                    {/* Inline display for the company overview */}
                    {overviews[job.company] && (
                        <div className="company-overview" style={{ marginTop: "15px", padding: "10px", backgroundColor: "#f0f4f8", borderRadius: "8px" }}>
                            <h4>Overview for {job.company}</h4>
                            <p style={{ whiteSpace: "pre-wrap", margin: 0 }}>{overviews[job.company]}</p>
                        </div>
                    )}

                    <div className="job-buttons" style={{ marginTop: "15px", display: "flex", gap: "10px" }}>
                        {job.link && (
                            <button
                                onClick={() => window.open(job.link, "_blank")}
                            >
                                Apply Now
                            </button>
                        )}

                        {job.company && (
                            <button
                                onClick={() => handleSearchOverview(job.company)}
                                disabled={loading[job.company]}
                            >
                                {loading[job.company] ? "Loading..." : "Search Overview"}
                            </button>
                        )}
                    </div>
                </section>
            ))}
        </div>
    );
}

export default JobList;