COURSE = {
    "id": "web_dev",
    "display_name": "Web Development",
    "description": "Build modern websites and applications",
    "icon": "🌐",
    "type": "web",
    
    "topics": {
        # TIER 1 - Foundations
        "html_basics": {
            "display_name": "HTML Fundamentals",
            "tier": 1,
            "prerequisites": [],
            "description": "Structure of the web",
            "key_concepts": ["Semantic HTML", "Forms", "Links/Images", "Tables", "Accessibility", "SEO basics"],
            "teaching_notes": "Semantic HTML (header/nav/main/article) is crucial for accessibility and SEO."
        },
        "css_basics": {
            "display_name": "CSS Fundamentals",
            "tier": 1,
            "prerequisites": ["html_basics"],
            "description": "Styling web pages",
            "key_concepts": ["Selectors", "Box model", "Flexbox", "Grid", "Responsive design", "CSS variables"],
            "teaching_notes": "Flexbox for 1D layouts, Grid for 2D. Mobile-first with media queries."
        },
        "javascript_basics": {
            "display_name": "JavaScript Basics",
            "tier": 1,
            "prerequisites": ["html_basics"],
            "description": "Making websites interactive",
            "key_concepts": ["DOM manipulation", "Events", "Variables/functions", "Arrays/Objects", "Async basics"],
            "teaching_notes": "Connect JS to HTML via querySelector and addEventListener immediately."
        },

        # TIER 2 - Intermediate
        "responsive_design": {
            "display_name": "Responsive Design",
            "tier": 2,
            "prerequisites": ["css_basics"],
            "description": "Mobile-friendly websites",
            "key_concepts": ["Media queries", "Mobile-first", "Viewport meta", "Fluid layouts", "Responsive images"],
            "teaching_notes": "Design for mobile first, then enhance for larger screens."
        },
        "react_basics": {
            "display_name": "React Fundamentals",
            "tier": 2,
            "prerequisites": ["javascript_basics"],
            "description": "Component-based UI library",
            "key_concepts": ["Components", "JSX", "Props", "State", "Hooks (useState/useEffect)", "Event handling"],
            "teaching_notes": "Components = reusable UI pieces. State triggers re-renders."
        },
        "api_integration": {
            "display_name": "API Integration",
            "tier": 2,
            "prerequisites": ["javascript_basics", "react_basics"],
            "description": "Fetching data from APIs",
            "key_concepts": ["fetch API", "async/await", "Promises", "REST", "Error handling", "Loading states"],
            "teaching_notes": "Always handle loading and error states. Use useEffect for API calls in React."
        },

        # TIER 3 - Advanced
        "backend_basics": {
            "display_name": "Backend with Node.js",
            "tier": 3,
            "prerequisites": ["javascript_basics", "api_integration"],
            "description": "Server-side JavaScript",
            "key_concepts": ["Express.js", "Routes", "Middleware", "REST APIs", "Environment variables", "CORS"],
            "teaching_notes": "Separate routes from business logic. Use express.Router() for organization."
        },
        "authentication": {
            "display_name": "Authentication",
            "tier": 3,
            "prerequisites": ["backend_basics"],
            "description": "User login and security",
            "key_concepts": ["JWT", "Session vs Token", "bcrypt", "Middleware auth", "OAuth basics"],
            "teaching_notes": "Never store plaintext passwords. Always hash with bcrypt/argon2."
        },
        "deployment": {
            "display_name": "Deployment",
            "tier": 3,
            "prerequisites": ["backend_basics", "react_basics"],
            "description": "Putting websites online",
            "key_concepts": ["Vercel/Netlify", "Environment config", "Build process", "Custom domains", "CI/CD basics"],
            "teaching_notes": "Vercel for frontend, Render/Fly.io for backend. Environment variables are critical."
        },
    }
}