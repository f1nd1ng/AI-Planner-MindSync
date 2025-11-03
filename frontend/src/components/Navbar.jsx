import { Link, NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="site-topbar">
      <div className="site-container topbar-inner">
        <Link to="/" className="brand">MindSync</Link>

        <nav className="nav-links">
          <NavLink to="/features">Features</NavLink>
          <NavLink to="/pricing">Pricing</NavLink>
          <NavLink to="/about">About</NavLink>
          <NavLink to="/contact">Contact</NavLink>
        </nav>

        <div className="nav-cta">
          <Link to="/signup" className="btn pill solid">Get Started</Link>
          <Link to="/login" className="btn text">Log in</Link>
        </div>
      </div>
    </header>
  );
}
