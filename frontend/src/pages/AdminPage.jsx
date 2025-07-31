
import './CandidateForm.css';
import React, { useState } from 'react';

export default function AdminPage() {
  const adminName = "Admin"; // Replace with dynamic name if needed
  const [cutoff, setCutoff] = useState(50);

  return (
    <div className="page">
      <div className="content" style={{ overflowY: 'unset' }}>
        <div className="top-bar">
          Welcome, {adminName}
        </div>

        <div className="upload-section" style={{ flexDirection: 'column', alignItems: 'stretch', gap: '2rem' }}>
          <div className="upload-box" style={{ width: '100%', marginBottom: '2rem' }}>
            {/* Removed Set Cutoff slider and label as requested */}
            <label className="upload-label" style={{ fontSize: '1.2rem' }}>Enter the job description</label>
            <textarea
              className="job-textarea"
              rows="14"
              placeholder="Type the full job description here..."
              style={{
                width: '100%',
                minHeight: '220px',
                fontSize: '1.1rem',
                padding: '1.25rem',
                border: '1px solid #ccc',
                borderRadius: '0.5rem',
                resize: 'vertical',
                background: 'rgba(255,255,255,0.7)',
                boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
