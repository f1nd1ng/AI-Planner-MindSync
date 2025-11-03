import React from "react";
import "../styles.css";

function Dashboard() {
  return (
    <div className="dashboard fade-in">
      <div className="nav">
        <h2 className="logo-text">MindSync</h2>
        <button className="logout-btn">Logout</button>
      </div>

      <div className="content">
        <h1>Welcome to your Smart Planner 🧠</h1>
        <p>
          This is your personalized AI-powered task planner. You’ll soon see your
          schedule, emotional trends, and smart task recommendations here.
        </p>
      </div>
    </div>
  );
}

export default Dashboard;
