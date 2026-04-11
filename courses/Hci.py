# courses/hci.py - Human-Computer Interaction Course Definition

COURSE = {
    "id": "hci",
    "display_name": "Human-Computer Interaction",
    "description": "Design principles, usability, and the science of user interfaces",
    "icon": "🖥️",
    "type": "theory",  # theory + discussion-based

    "topics": {
        "hci_intro": {
            "display_name": "What is HCI?",
            "tier": 1,
            "prerequisites": [],
            "description": "Overview of HCI as a discipline",
            "key_concepts": ["Definition of HCI", "Interdisciplinary nature",
                             "History of HCI", "Goals of HCI", "HCI vs UX vs UI"],
            "teaching_notes": "Get students thinking about bad interfaces they've used. Frustration is relatable."
        },
        "usability": {
            "display_name": "Usability Principles",
            "tier": 1,
            "prerequisites": ["hci_intro"],
            "description": "What makes an interface usable",
            "key_concepts": ["Nielsen's 10 Usability Heuristics", "Learnability",
                             "Efficiency", "Memorability", "Errors", "Satisfaction",
                             "ISO 9241 usability definition"],
            "teaching_notes": "Nielsen's heuristics are the most-tested topic in HCI exams. Teach all 10."
        },
        "user_centred_design": {
            "display_name": "User-Centred Design (UCD)",
            "tier": 1,
            "prerequisites": ["usability"],
            "description": "Designing with the user at the centre",
            "key_concepts": ["UCD process", "Requirements gathering", "Personas",
                             "User stories", "Iterative design", "Contextual inquiry"],
            "teaching_notes": "Personas are often exam questions. Emphasise the iterative design cycle."
        },
        "mental_models": {
            "display_name": "Mental Models & Affordances",
            "tier": 2,
            "prerequisites": ["hci_intro"],
            "description": "How users think about and perceive interfaces",
            "key_concepts": ["Mental model", "Conceptual model", "Affordance",
                             "Signifier", "Mapping", "Feedback", "Constraints",
                             "Gulf of execution", "Gulf of evaluation"],
            "teaching_notes": "Don Norman's concepts. The door handle example (push vs pull) is classic."
        },
        "interaction_styles": {
            "display_name": "Interaction Styles",
            "tier": 2,
            "prerequisites": ["usability"],
            "description": "Different ways humans interact with computers",
            "key_concepts": ["Command line", "Menus", "Form fill-in", "Direct manipulation",
                             "WIMP (Windows, Icons, Menus, Pointers)", "Touch", "Voice", "Gestures"],
            "teaching_notes": "Connect to interfaces students use daily — phone vs desktop vs smart speaker."
        },
        "prototyping": {
            "display_name": "Prototyping",
            "tier": 2,
            "prerequisites": ["user_centred_design"],
            "description": "Building early versions to test ideas",
            "key_concepts": ["Low-fidelity (paper) prototypes", "High-fidelity prototypes",
                             "Wireframes", "Mockups", "Storyboards",
                             "Prototype fidelity tradeoffs"],
            "teaching_notes": "Paper prototyping exercise is a classic practical. Emphasise testing with real users."
        },
        "evaluation_methods": {
            "display_name": "Evaluation Methods",
            "tier": 3,
            "prerequisites": ["usability", "prototyping"],
            "description": "How to test if interfaces work",
            "key_concepts": ["Usability testing", "Think-aloud protocol", "Heuristic evaluation",
                             "Cognitive walkthrough", "A/B testing", "Analytics",
                             "Formative vs summative evaluation"],
            "teaching_notes": "Heuristic evaluation and usability testing are the most common exam topics."
        },
        "accessibility": {
            "display_name": "Accessibility & Inclusive Design",
            "tier": 2,
            "prerequisites": ["usability"],
            "description": "Designing for all users including those with disabilities",
            "key_concepts": ["WCAG guidelines", "Screen readers", "Colour contrast",
                             "Motor impairments", "Cognitive accessibility",
                             "Universal design principles"],
            "teaching_notes": "Accessibility is increasingly in exams and industry. WCAG 2.1 is the standard."
        },
        "information_architecture": {
            "display_name": "Information Architecture",
            "tier": 3,
            "prerequisites": ["interaction_styles"],
            "description": "Organising and structuring information in interfaces",
            "key_concepts": ["Navigation design", "Card sorting", "Site maps",
                             "Taxonomy", "Labelling systems", "Search systems",
                             "Wayfinding"],
            "teaching_notes": "Card sorting is a practical exercise worth doing. Connects to real web design."
        },
        "colour_typography": {
            "display_name": "Visual Design: Colour & Typography",
            "tier": 2,
            "prerequisites": ["hci_intro"],
            "description": "Principles of visual communication in interfaces",
            "key_concepts": ["Colour theory", "Contrast ratios", "Typography hierarchy",
                             "Gestalt principles", "Visual hierarchy", "White space"],
            "teaching_notes": "Gestalt principles (proximity, similarity, closure) frequently appear in exams."
        },
    }
}