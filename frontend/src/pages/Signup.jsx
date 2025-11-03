import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles.css";

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirm: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (form.password !== form.confirm) {
      alert("Passwords do not match");
      return;
    }
    navigate("/");
  };

  return (
    <div className="page-root">
      {/* Top bar */}
      

      {/* Body layout */}
      <main className="auth-wrap">
        <div className="auth-shell">

          {/* Left Illustration Panel */}
          <section className="art-panel">
            <div className="art-circle" />
            <div
              className="ill-card"
              role="img"
              aria-label="Cozy study illustration"
              style={{ backgroundImage: 'url("/assets/login-illustration.png")' }}
            />
          </section>

          {/* Right Form Panel */}
          <section className="form-panel">
            <h2 className="form-title">Create Account</h2>

            <form onSubmit={handleSubmit} className="form">
              <input
                type="text"
                placeholder="Full Name"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />

              <input
                type="email"
                placeholder="E-mail"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />

              <input
                type="password"
                placeholder="Set Password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />

              <input
                type="password"
                placeholder="Confirm Password"
                value={form.confirm}
                onChange={(e) => setForm({ ...form, confirm: e.target.value })}
                required
              />

              <button type="submit" className="primary-btn">Sign up</button>
            </form>

            <p className="muted">
              Already have an account?{" "}
              <Link to="/" className="link">Login</Link>
            </p>
          </section>
        </div>
      </main>
    </div>
  );
}
