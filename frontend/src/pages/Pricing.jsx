export default function Pricing() {
  return (
    <section className="section">
      <div className="site-container pricing">
        <h2>Pricing</h2>
        <div className="pricing-grid">
          <div className="price-card">
            <h3>Free</h3>
            <p className="price">$0</p>
            <ul>
              <li>Daily planner</li>
              <li>Mood check-ins</li>
              <li>Local calendar</li>
            </ul>
          </div>
          <div className="price-card highlight">
            <h3>Pro</h3>
            <p className="price">$6/mo</p>
            <ul>
              <li>Google Calendar sync</li>
              <li>Priority & focus modes</li>
              <li>Unlimited tasks</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
