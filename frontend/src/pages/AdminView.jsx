import './CandidateForm.css';
import React, { useState } from 'react';

// Example candidate data (replace with API data as needed)
const candidates = [
  {
    id: 1,
    name: 'Abhijith',
    score: 87,
    resumeUrl: 'https://example.com/resume/abhijith.pdf',
    accepted: null
  },
  {
    id: 2,
    name: 'Bimal',
    score: 72,
    resumeUrl: 'https://example.com/resume/bimal.pdf',
    accepted: null
  },
  {
    id: 3,
    name: 'Aravindh',
    score: 94,
    resumeUrl: 'https://example.com/resume/aravindh.pdf',
    accepted: null
  },
  {
    id: 4,
    name: 'Hormis',
    score: 81,
    resumeUrl: 'https://example.com/resume/hormis.pdf',
    accepted: null
  },
  {
    id: 5,
    name: 'Bilal',
    score: 65,
    resumeUrl: 'https://example.com/resume/bilal.pdf',
    accepted: null
  }
];

export default function AdminView() {
  const [candidateList, setCandidateList] = useState(candidates);

  const handleDecision = (id, accepted) => {
    setCandidateList(prev => prev.map(c =>
      c.id === id ? { ...c, accepted } : c
    ));
  };

  return (
    <div className="page">
      <div className="content" style={{ padding: '2rem' }}>
        <div className="top-bar" style={{ marginBottom: '2rem', color: '#2563eb', background: 'rgba(37,99,235,0.08)', fontWeight: 700 }}>
          Candidate Applications
        </div>
        <div style={{ width: '100%', maxWidth: 900, margin: '0 auto' }}>
          <table style={{ width: '100%', background: 'rgba(255,255,255,0.8)', borderRadius: '0.75rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', borderCollapse: 'collapse', overflow: 'hidden' }}>
            <thead>
              <tr style={{ background: 'rgba(37,99,235,0.15)' }}>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '1rem', textAlign: 'center' }}>Score</th>
                <th style={{ padding: '1rem', textAlign: 'center' }}>Resume</th>
                <th style={{ padding: '1rem', textAlign: 'center' }}>Accept</th>
                <th style={{ padding: '1rem', textAlign: 'center' }}>Reject</th>
              </tr>
            </thead>
            <tbody>
              {candidateList.map(candidate => (
                <tr key={candidate.id} style={{ borderBottom: '1px solid #e0e7ef' }}>
                  <td style={{ padding: '1rem', fontWeight: 600 }}>{candidate.name}</td>
                  <td style={{ padding: '1rem', textAlign: 'center', color: '#2563eb', fontWeight: 700 }}>{candidate.score}</td>
                  <td style={{ padding: '1rem', textAlign: 'center' }}>
                    <a href={candidate.resumeUrl} target="_blank" rel="noopener noreferrer" style={{ color: '#2563eb', textDecoration: 'underline', fontWeight: 500 }}>View Resume</a>
                  </td>
                  <td style={{ padding: '1rem', textAlign: 'center' }}>
                    <input
                      type="checkbox"
                      checked={candidate.accepted === true}
                      onChange={() => handleDecision(candidate.id, true)}
                      style={{ width: 20, height: 20, accentColor: '#22c55e' }}
                    />
                  </td>
                  <td style={{ padding: '1rem', textAlign: 'center' }}>
                    <input
                      type="checkbox"
                      checked={candidate.accepted === false}
                      onChange={() => handleDecision(candidate.id, false)}
                      style={{ width: 20, height: 20, accentColor: '#ef4444' }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
            <button
              style={{
                background: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                padding: '0.75rem 2.5rem',
                fontWeight: 700,
                fontSize: '1.1rem',
                cursor: 'pointer',
                boxShadow: '0 1px 4px rgba(37,99,235,0.08)'
              }}
            >
              Confirm
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
