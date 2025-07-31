import './CandidateForm.css';
import React from 'react';

// Example jobs data (replace with API data as needed)
const jobs = [
  {
    id: 1,
    title: 'Frontend Developer',
    company: 'Tech Solutions',
    location: 'Remote',
    description: 'Work on modern React apps with a dynamic team.'
  },
  {
    id: 2,
    title: 'Backend Engineer',
    company: 'DataWorks',
    location: 'Bangalore',
    description: 'Build scalable APIs and microservices.'
  },
  {
    id: 3,
    title: 'UI/UX Designer',
    company: 'Creative Minds',
    location: 'Delhi',
    description: 'Design beautiful and user-friendly interfaces.'
  }
];

export default function Candidate1() {
  const candidateName = "Abhijith"; // Replace with actual user data

  return (
    <div className="page">
      <div className="content">
        <div className="top-bar">
          Welcome, {candidateName}
        </div>

        <div className="upload-section" style={{ flexDirection: 'column', alignItems: 'stretch', gap: '2rem' }}>
          <div style={{ width: '100%' }}>
            <h2 style={{ color: '#2563eb', marginBottom: '1.5rem', textAlign: 'center', fontWeight: 700 }}>Available Jobs</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              {jobs.map(job => (
                <div key={job.id} style={{
                  background: 'rgba(255,255,255,0.7)',
                  borderRadius: '0.75rem',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  padding: '1.5rem 2rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.5rem',
                }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 600, color: '#222' }}>{job.title}</div>
                  <div style={{ color: '#2563eb', fontWeight: 500 }}>{job.company} &mdash; {job.location}</div>
                  <div style={{ color: '#444', fontSize: '1rem' }}>{job.description}</div>
                  <button style={{
                    marginTop: '0.75rem',
                    alignSelf: 'flex-end',
                    background: '#2563eb',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    padding: '0.5rem 1.5rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    fontSize: '1rem',
                    boxShadow: '0 1px 4px rgba(37,99,235,0.08)'
                  }}>Apply</button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
