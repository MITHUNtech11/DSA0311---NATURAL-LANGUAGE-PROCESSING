"""
Course: DSA0311 - Natural Language Processing
Assessment: CO1 - Assessment Tool 1 (Application Based Questions)
Section 1: Regular Expressions – Resume Information Extraction
"""

import re
from typing import Dict, List, Any

class ResumeInformationExtractor:
    """
    Automated Resume Information Extraction System using Regular Expressions.
    Extracts candidate name, email, mobile number, technical skills, and years of experience.
    """
    def __init__(self):
        # 1. Candidate Name: extracts name following explicit labels up to newline
        self.name_pattern = re.compile(
            r'(?:Name|Candidate Name|Full Name):\s*([A-Za-z\.\s]+?)(?=\s*(?:\r?\n|$))',
            re.IGNORECASE
        )
        
        # 2. Email Address: standard RFC compliant email pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        )
        
        # 3. Mobile Number: supports optional +91 or 0 prefix followed by 10 digits starting with 6-9
        self.phone_pattern = re.compile(
            r'(?:(?:\+91|0)?[\s-]?)?[6-9]\d{9}'
        )
        
        # 4. Technical Skills: targeted skills using word boundaries to avoid false substring matches
        self.skills_pattern = re.compile(
            r'\b(Python|Java|SQL|Machine\s+Learning|NLP)\b',
            re.IGNORECASE
        )
        
        # 5. Experience: captures integer or decimal experience followed by year/yrs keyword
        self.exp_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?',
            re.IGNORECASE
        )
        
        # Skill normalization dictionary
        self.skill_norm = {
            "python": "Python",
            "java": "Java",
            "sql": "SQL",
            "machine learning": "Machine Learning",
            "nlp": "NLP"
        }

    def extract_profile(self, resume_text: str) -> Dict[str, Any]:
        """Extracts structured candidate profile from raw resume text."""
        # Extract Candidate Name
        name_match = self.name_pattern.search(resume_text)
        name = name_match.group(1).strip() if name_match else "Not Found"
        
        # Extract Email
        email_match = self.email_pattern.search(resume_text)
        email = email_match.group(0).strip() if email_match else "Not Found"
        
        # Extract Mobile Number
        phone_match = self.phone_pattern.search(resume_text)
        phone = phone_match.group(0).strip() if phone_match else "Not Found"
        
        # Detect Technical Skills
        raw_skills = self.skills_pattern.findall(resume_text)
        normalized_skills = sorted(list({self.skill_norm[s.lower()] for s in raw_skills}))
        
        # Extract Years of Experience
        exp_match = self.exp_pattern.search(resume_text)
        experience = float(exp_match.group(1)) if exp_match else 0.0
        
        # Evaluate Eligibility: Minimum 2.0 years experience AND Python skill
        is_eligible = (experience >= 2.0) and ("Python" in normalized_skills)
        eligibility_reason = []
        if experience < 2.0:
            eligibility_reason.append(f"Insufficient experience ({experience} yrs < 2.0 yrs required)")
        if "Python" not in normalized_skills:
            eligibility_reason.append("Missing mandatory 'Python' skill")
        if is_eligible:
            eligibility_reason.append("Satisfies all eligibility requirements")

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": normalized_skills,
            "experience_years": experience,
            "eligible": is_eligible,
            "remarks": "; ".join(eligibility_reason)
        }

def run_experiment():
    resumes = [
        """Name: Dr. Sarah Jenkins
Email: sarah.jenkins@techcorp.com
Phone: +91 9876543210
Summary: Senior AI Researcher with strong expertise in Python, Machine Learning, and NLP.
Experience: 4.5 years of industry experience building end-to-end NLP pipelines.""",

        """Candidate Name: Rajesh Kumar
Email: rajesh.k@innovate.org
Contact: 8765432109
Skills: Core Java, SQL database management, Spring Boot, Microservices.
Work History: 3.0 years of experience in enterprise backend engineering.""",

        """Full Name: Priya Sharma
Email: priya.sharma@aimodels.io
Mobile: +91-7654321098
Technical Competencies: Python, NLP, PyTorch, Deep Learning.
Professional Experience: 1.2 years of experience as a junior NLP engineer.""",

        """Name: Michael Chang
Email: mchang@datasolutions.net
Phone: 9123456780
Skills: Proficient in Python, SQL, Java, Machine Learning, Docker.
Experience: 2.0+ years of experience delivering predictive analytics models."""
    ]

    extractor = ResumeInformationExtractor()
    print("=" * 75)
    print("     AUTOMATED RESUME INFORMATION EXTRACTION & SCREENING SYSTEM")
    print("=" * 75)

    all_profiles = [extractor.extract_profile(r) for r in resumes]

    for i, p in enumerate(all_profiles, 1):
        print(f"\n[Candidate Profile {i}]")
        print(f"  Name              : {p['name']}")
        print(f"  Email             : {p['email']}")
        print(f"  Mobile Number     : {p['phone']}")
        print(f"  Technical Skills  : {', '.join(p['skills']) if p['skills'] else 'None Detected'}")
        print(f"  Experience        : {p['experience_years']} Year(s)")
        print(f"  Shortlist Status  : {'SHORTLISTED (ELIGIBLE)' if p['eligible'] else 'REJECTED (INELIGIBLE)'}")
        print(f"  Remarks           : {p['remarks']}")

    print("\n" + "=" * 75)
    print("             HR SHORTLISTING SUMMARY REPORT")
    print("=" * 75)
    print(f"{'Name':<20} | {'Experience':<12} | {'Python Skill':<14} | {'Status'}")
    print("-" * 75)
    for p in all_profiles:
        has_py = "Yes" if "Python" in p["skills"] else "No"
        status = "ELIGIBLE" if p["eligible"] else "NOT ELIGIBLE"
        print(f"{p['name']:<20} | {p['experience_years']:<4} yrs      | {has_py:<14} | {status}")
    print("=" * 75)

if __name__ == "__main__":
    run_experiment()
