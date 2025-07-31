import './AdminPage.css';

export default function AdminPage() {
  const adminName = "Admin"; // Replace with dynamic name if needed

  return (
    <div className="admin-page">
      <div className="top-bar">
        <span className="welcome-text">Welcome, {adminName}</span>
      </div>

      <div className="job-section">
        <label className="job-label">Enter the job description</label>
        <textarea
          className="job-textarea"
          rows="10"
          placeholder="Type the full job description here..."
        />
      </div>
    </div>
  );
}
