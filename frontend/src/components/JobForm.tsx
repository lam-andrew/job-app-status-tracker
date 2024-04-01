import React, { useState, FormEvent } from 'react';
import axios from 'axios';

type ApplicationStatus = 
    | 'Applied'
    | 'Under Review'
    | 'Interview Scheduled'
    | 'Interview Completed'
    | 'Offer Extended'
    | 'Offer Accepted'
    | 'Offer Declined'
    | 'Rejected'
    | 'Withdrawn'
    | 'On Hold';

interface JobJsonResponse {
    JobTitle: string | null;
    CompanyName: string | null;
    Location: string | null;
    WorkFormat: 'Full-Time' | 'Part-Time' | 'Contract' | 'Internship' | null;
    RemoteWorkAvailability: 'Onsite' | 'Remote' | 'Hybrid' | null;
    ApplicationDeadline: string | null; // Assuming ISO date format or null
    ApplicationDate: string; // Assuming ISO date format
    SalaryRange: string | null;
    RequiredSkills: string[] | null;
    Benefits: string[] | null;
    ApplicationStatus: ApplicationStatus;
    AdditionalDetails: {
        ApplicationLink: string | null;
        [key: string]: any; // For any additional, unexpected fields
    };
}

interface ApiResponse {
    message: string;
    job_json: JobJsonResponse;
    current_date: string;
}

const JobForm: React.FC = () => {
    const [jobDesc, setJobDesc] = useState<string>('');
    const [response, setResponse] = useState<ApiResponse | null>(null);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        try {
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_ENDPOINT}/insert_job`, {
                job_desc_input: jobDesc,
                current_date: new Date().toISOString()
            });
            setResponse(response.data)
        } catch (error) {
            console.error("Error sending job description:", error);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit}>
                <label>
                    Job Description:
                    <textarea value={jobDesc} onChange={(e) => setJobDesc(e.target.value)} />
                </label>
                <button type="submit">Submit</button>
            </form>

            {response && (
                <div>
                    <h2>Response:</h2>
                    <p>Message: {response.message}</p>
                    <p>Job JSON: {JSON.stringify(response.job_json, null, 2)}</p>
                    <p>Current Date: {response.current_date}</p>
                </div>
            )}
        </>
        
    );
};

export default JobForm;
