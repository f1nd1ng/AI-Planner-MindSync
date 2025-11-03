import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/Home");
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
            {/* full-bleed illustrated card */}
            <div
              className="ill-card"
              role="img"
              aria-label="Cozy study illustration"
              style={{ backgroundImage: 'url("/assets/login-illustration.png")' }} // public/ path
            />
          </section>

          {/* Right Form Panel */}
          <section className="form-panel">
            <h2 className="form-title">Sign In</h2>

            <form onSubmit={handleSubmit} className="form">
              <input
                type="email"
                placeholder="Enter E-mail"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <input
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              <div className="aux-row">
                <button type="button" className="link-sm">Forgot password?</button>
              </div>

              <div className="divider"><span>Or</span></div>

              <button type="button" className="google-btn">
                Login with Google
              </button>

              <button type="submit" className="primary-btn">Login</button>
            </form>

            <p className="muted">
              Don’t have an account?{" "}
              <Link to="/signup" className="link">Sign up</Link>
            </p>
          </section>
        </div>
      </main>
    </div>
  );
}
