import { Link } from "react-router-dom";

export default function Home() {
  return (
    <>
      {/* Hero */}
      <section className="hero">
        <div className="site-container hero-grid">
          <div className="hero-copy">
            <h1 style={{ 
            fontFamily: "'Times New Roman', serif",
            fontWeight: 600,
            fontSize: "50px",
            color: "#0F3B2E",
            letterSpacing: "-0.5px",
            
            }}>
            Plan tasks that match<br></br> your mood.
            </h1>

            <p 
            className="lead" 
            style={{ fontFamily: "'Times New Roman', serif",
                fontSize: 20,
                paddingBottom: "40px",
                
             }}
            >
            work smarter, avoid burnout, and keep momentum.
            </p>

            <div className="cta-row">
              <Link to="/signup" className="btn primary">Get Started</Link>
              <Link to="/features" className="btn ghost">See Features</Link>
            </div>
          </div>

          <div className="hero-art">
            <div className="hero-card" style={{backgroundImage:'url(/assets/login-illustration.png)'}} />
          </div>
        </div>
      </section>

      {/* Feature strip */}
      <section className="section">
        <div className="site-container feature-grid">
          <div className="feature">
            <h3>Understand your energy</h3>
            <p>Quick check-ins map your mood to the right kind of work.</p>
          </div>
          <div className="feature">
            <h3>Automatic time blocks</h3>
            <p>We lay out your day with realistic breaks and buffers.</p>
          </div>
          <div className="feature">
            <h3>Calendar sync</h3>
            <p>Export to Google Calendar with one click.</p>
          </div>
        </div>
      </section>
    </>
  );
}
