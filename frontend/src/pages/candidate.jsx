import './CandidateForm.css';

export default function CandidateForm() {
  const candidateName = "Abhijith"; // Replace this with dynamic value if needed

  return (
    <div className="page">
      <div className="top-bar">
        <span className="welcome-text">Welcome, {candidateName}</span>
      </div>

      <div className="upload-section">
        <label className="upload-label">Upload Resume</label>
        <input type="file" className="upload-input" />
      </div>
    </div>
  );
}
