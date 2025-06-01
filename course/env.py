from prompt import get_all_prompts
from environment import BaseEnv


class OnlineCourse(BaseEnv):
    items = {
        "data science": [
            ("Hands-on projects with real datasets", "Purely theoretical video lectures", "Project style not specified"),
            ("Instructors from top tech firms", "Instructors with limited industry experience", "Instructor background not specified"),
            ("Career-recognised certificate awarded", "No certificate provided", "Certification not specified"),
            ("Coverage of key tools (Pandas, TensorFlow, Spark)", "Tool coverage is superficial", "Tool coverage not specified"),
            ("Detailed rubric-based feedback on assignments", "Automated generic feedback only", "Feedback policy not specified"),
            ("Capstone project reviewed by experts", "Automated grading only", "Capstone review not specified"),
            ("Lifetime access and free updates", "Access expires after a year", "Access duration not specified"),
            ("Active peer discussion forums", "No peer-to-peer interaction", "Community support not specified"),
        ],

        "web development": [
            ("Project-based full-stack curriculum", "Frontend HTML/CSS only", "Curriculum depth not specified"),
            ("Live coding support sessions", "No live support", "Support availability not specified"),
            ("Covers popular frameworks (React, Node)", "Outdated technologies taught", "Framework coverage not specified"),
            ("Portfolio website built during course", "No portfolio output", "Portfolio deliverable not specified"),
            ("Job-placement assistance on completion", "No career services", "Career services not specified"),
            ("Industry mentors for code reviews", "Peer-only code reviews", "Mentoring not specified"),
            ("Regular quizzes and coding challenges", "Few or no assessments", "Assessment frequency not specified"),
            ("Lifetime course access", "Access limited to six months", "Access period not specified"),
        ],

        "business & management": [
            ("Case studies from Fortune 500 companies", "Generic textbook examples", "Case-study source not specified"),
            ("Live webinars with C-suite executives", "Pre-recorded lectures only", "Webinar format not specified"),
            ("Globally recognised professional certificate", "Unaccredited certificate", "Certification status not specified"),
            ("Assignments graded by industry experts", "Automated grading only", "Grading method not specified"),
            ("Networking events with alumni", "No networking opportunities", "Networking not specified"),
            ("Focus on leadership and strategic thinking", "Limited strategic content", "Content focus not specified"),
            ("Downloadable business toolkits", "No supplementary resources", "Resource availability not specified"),
            ("Content updated each quarter", "Rarely updated content", "Update frequency not specified"),
        ],

        "graphic design": [
            ("Portfolio-building practical projects", "Theory-heavy lectures", "Project emphasis not specified"),
            ("Taught by award-winning designers", "Instructors without notable awards", "Instructor accolades not specified"),
            ("Includes Adobe Creative Cloud training", "Uses only free software", "Software coverage not specified"),
            ("Interactive design critiques", "No formal critique sessions", "Critique format not specified"),
            ("Professional certification issued", "No certification", "Certification not specified"),
            ("Lifetime access with future updates", "Limited access window", "Access details not specified"),
            ("Job placement resources and guidance", "No job placement support", "Career support not specified"),
            ("Exclusive design assets provided", "Only publicly available assets", "Asset exclusivity not specified"),
        ],

        "cybersecurity": [
            ("Hands-on labs simulating real attacks", "Lecture-only content", "Lab component not specified"),
            ("Instructors are certified security experts", "General IT instructors", "Instructor expertise not specified"),
            ("Prepares for CEH / CISSP exams", "No exam alignment", "Exam alignment not specified"),
            ("Real-world breach case studies", "Hypothetical examples only", "Case-study realism not specified"),
            ("Live Q&A with ethical hackers", "No live Q&A sessions", "Q&A availability not specified"),
            ("Comprehensive tool coverage (Wireshark, Metasploit)", "Limited tool demonstrations", "Tool coverage not specified"),
            ("Lifetime updates and access", "Access expires after one year", "Access term not specified"),
            ("Career coaching and résumé review", "No career coaching", "Career services not specified"),
        ],

        "digital marketing": [
            ("Campaigns built on real ad platforms", "Simulated campaigns only", "Campaign realism not specified"),
            ("Google-certified instructors", "Uncertified instructors", "Instructor certification not specified"),
            ("Includes SEO, SEM, and social media modules", "Covers only basic social media", "Module breadth not specified"),
            ("Live critique of student ad copy", "No live critique", "Critique format not specified"),
            ("Certification recognised by employers", "Certificate not widely recognised", "Certification recognition not specified"),
            ("Access to premium marketing tools", "Only free-tool demos", "Tool access not specified"),
            ("Alumni community for job referrals", "No alumni network", "Community access not specified"),
            ("Course content updated monthly", "Rarely updated content", "Update schedule not specified"),
        ],

        "finance & investing": [
            ("Real-time market simulations", "Historical data only", "Simulation type not specified"),
            ("Taught by CFA-charterholders", "Instructors without finance credentials", "Instructor credentials not specified"),
            ("Certification in financial modelling", "No formal certification", "Certification not specified"),
            ("Case studies on portfolio management", "Basic theory, few cases", "Case-study depth not specified"),
            ("Interactive Excel/Sheets templates", "Minimal downloadable templates", "Template availability not specified"),
            ("Live Q&A with investment analysts", "No live sessions", "Live session availability not specified"),
            ("Lifetime video and resource access", "Access time-limited", "Resource access not specified"),
            ("Career services for finance roles", "No career services", "Career services not specified"),
        ],

        "artificial intelligence": [
            ("Hands-on neural-network projects", "Slides-only theoretical lectures", "Project type not specified"),
            ("Uses PyTorch & TensorFlow frameworks", "Uses outdated or proprietary tools", "Framework coverage not specified"),
            ("Capstone reviewed by AI professionals", "Peer review only", "Capstone review not specified"),
            ("Includes responsible-AI and ethics module", "Ethics module omitted", "Ethics coverage not specified"),
            ("Access to GPU cloud credits", "No cloud-compute access", "Compute access not specified"),
            ("Mentor support via weekly office hours", "No mentor support", "Mentor availability not specified"),
            ("Certificate accepted by tech employers", "Unaccredited certificate", "Certificate status not specified"),
            ("Lifetime access with quarterly updates", "Static content, no updates", "Content update not specified"),
        ],

        "cloud computing": [
            ("Hands-on labs on AWS / Azure / GCP", "Slide-only demonstrations", "Lab component not specified"),
            ("Instructors with cloud-architect certifications", "Instructors without cloud certs", "Instructor certification not specified"),
            ("Prepares for AWS/Azure architect exams", "No exam preparation", "Exam prep not specified"),
            ("Sandbox credits for live cloud deployment", "No cloud credits provided", "Sandbox access not specified"),
            ("Covers DevOps and CI/CD pipelines", "DevOps topics omitted", "DevOps coverage not specified"),
            ("Live troubleshooting sessions", "No live troubleshooting", "Live support not specified"),
            ("Infrastructure-as-code projects (Terraform)", "No IaC projects", "IaC coverage not specified"),
            ("Lifetime access with ongoing cloud updates", "Content rarely updated", "Update frequency not specified"),
        ],

        "project management": [
            ("PMP-aligned curriculum", "No certification alignment", "Curriculum alignment not specified"),
            ("Agile & Scrum simulations", "Lecture-only agile overview", "Agile coverage not specified"),
            ("Real-world project capstone", "No capstone project", "Capstone availability not specified"),
            ("1-to-1 mentor feedback on project plans", "Self-graded plans only (no mentor feedback)", "Feedback availability not specified"),
            ("Risk-management deep dive", "Risk topic lightly covered", "Risk coverage not specified"),
            ("Stakeholder communication role-plays", "No communication practice", "Communication practice not specified"),
            ("Access to PM tools (Jira, MS Project)", "Tool demos only", "Tool access not specified"),
            ("Career coaching for PM roles", "No career services", "Career services not specified"),
        ],
    }

    prices = {
        "data science":            [(1500, 2000), (700, 1000), (200, 400)],
        "web development":         [(1200, 1700), (600, 900),  (150, 350)],
        "business & management":   [(1800, 2500), (900, 1300), (300, 500)],
        "graphic design":          [(1000, 1400), (500, 800),  (150, 300)],
        "cybersecurity":           [(1600, 2200), (800, 1200), (250, 450)],
        "digital marketing":       [(1200, 1600), (550, 850),  (150, 300)],
        "finance & investing":     [(1500, 2000), (700, 1000), (200, 400)],
        "artificial intelligence": [(1700, 2300), (800, 1200), (250, 450)],
        "cloud computing":         [(1600, 2200), (800, 1200), (250, 450)],
        "project management":      [(1400, 1800), (700, 1000), (200, 400)],
    }
    all_prompts = get_all_prompts()