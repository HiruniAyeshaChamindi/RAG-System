import './Header.css'; // We'll create this CSS file next

const Header = () => {
return (
    <header
        className="app-header"
        style={{
            backgroundImage: "/images/images(1).jpeg",
            backgroundSize: "cover",
            backgroundPosition: "center",
        }}
    >
        <div className="university-info">
            <img
                src="/images/images.jpeg"
                alt="University of Moratuwa Logo"
                className="university-logo"
            />
            <h1 className="university-name">University of Moratuwa</h1>
            <div className="ai-assistant">
                <span>AI-Powered Academic Assistant</span>
            </div>
        </div>
        
        <div className="header-divider"></div>
        
        <div className="live-questions">
            <h2>Questions</h2>
        </div>
    </header>
);
};

export default Header;