import './CandidateForm.css';

export default function Candidate() {
  const candidateName = "Abhijith";

  return (
    <div className="page">
      <div className="content">
        <div className="top-bar">
          Welcome, {candidateName}
        </div>

        <div className="upload-section">
          <div className="upload-box">
            <label className="upload-label">Upload Resume</label>
            <input type="file" className="upload-input" />
          </div>
        </div>
      </div>
    </div>
  );
}
