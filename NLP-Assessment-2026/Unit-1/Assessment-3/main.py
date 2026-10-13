"""
Course: DSA0311 - Natural Language Processing
Assessment: CO1 - Assessment Tool 1 (Application Based Questions)
Section 3: Regular Expressions – University Registration System
"""

import re
from typing import Dict, List, Any

class UniversityRegistrationValidator:
    """
    Automated Student Online Registration Portal Validator using Regular Expressions.
    Validates register number, institutional email, course code, semester, and mobile number.
    """
    def __init__(self):
        # 1. Register Number: 12-digit enrollment ID or standard departmental format (e.g., 192111101045 or 21AD0101)
        self.reg_no_pattern = re.compile(
            r'^(?:\d{12}|[0-9]{2}[A-Z]{2,4}\d{3,4})$'
        )
        
        # 2. Institutional Email: restricted strictly to university educational domains
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)*(?:saveetha\.com|university\.ac\.in|institution\.edu)$',
            re.IGNORECASE
        )
        
        # 3. Course Code: 2-4 uppercase department characters followed by 2-4 digits (e.g., DSA03, CS101)
        self.course_pattern = re.compile(
            r'^[A-Z]{2,4}\d{2,4}$'
        )
        
        # 4. Semester: values bounded strictly between 1 and 8
        self.semester_pattern = re.compile(
            r'^(?:(?:Semester|Sem)\s*)?([1-8])$',
            re.IGNORECASE
        )
        
        # 5. Mobile Number: Indian 10-digit mobile number with optional +91 prefix
        self.mobile_pattern = re.compile(
            r'^(?:\+91[\-\s]?)?[6-9]\d{9}$'
        )

    def validate_student(self, student: Dict[str, str]) -> Dict[str, Any]:
        """Validates all registration fields and generates granular diagnostics."""
        errors = {}
        
        # 1. Validate Register Number
        if not self.reg_no_pattern.match(student.get("reg_no", "").strip()):
            errors["reg_no"] = "Invalid Register Number. Expected 12 digits or standard format (e.g., 192111101045 or 21AD0101)."
            
        # 2. Validate Institutional Email
        if not self.email_pattern.match(student.get("email", "").strip()):
            errors["email"] = "Invalid Institutional Email. Domain must be @saveetha.com, @university.ac.in, or @institution.edu."
            
        # 3. Validate Course Code
        if not self.course_pattern.match(student.get("course_code", "").strip()):
            errors["course_code"] = "Invalid Course Code. Format must be 2-4 uppercase department letters + 2-4 digits (e.g., DSA03, CS101)."
            
        # 4. Validate Semester
        sem_str = student.get("semester", "").strip()
        sem_match = self.semester_pattern.match(sem_str)
        if not sem_match:
            errors["semester"] = f"Invalid Semester '{sem_str}'. Must be an integer between 1 and 8 (e.g., 'Semester 6', 'Sem 4', or '6')."
            
        # 5. Validate Mobile Number
        if not self.mobile_pattern.match(student.get("mobile", "").strip()):
            errors["mobile"] = "Invalid Mobile Number. Must be a valid 10-digit number starting with 6-9, optionally with +91 country code."
            
        is_success = len(errors) == 0
        
        return {
            "name": student.get("name", "Unknown"),
            "data": student,
            "is_valid": is_success,
            "errors": errors,
            "status": "REGISTRATION SUCCESSFUL" if is_success else "REGISTRATION FAILED"
        }

def run_experiment():
    students_test_data = [
        {
            "name": "Aravind Swaminathan",
            "reg_no": "192111101045",
            "email": "aravind.s@saveetha.com",
            "course_code": "DSA03",
            "semester": "Semester 6",
            "mobile": "+91 9840123456"
        },
        {
            "name": "Sneha Patel",
            "reg_no": "21AD0102",
            "email": "sneha.patel@gmail.com",         # Invalid: Public email provider
            "course_code": "DSA03",
            "semester": "Semester 9",                # Invalid: Exceeds 8 semesters
            "mobile": "5840123456"                   # Invalid: Starts with 5
        },
        {
            "name": "Karthik Raja",
            "reg_no": "REG_INVALID_99",              # Invalid: Incorrect format
            "email": "karthik.r@university.ac.in",
            "course_code": "DSA_03_NLP",             # Invalid: Contains underscores/improper format
            "semester": "Sem 4",
            "mobile": "+91-8765432109"
        }
    ]

    validator = UniversityRegistrationValidator()
    print("=" * 80)
    print("      AUTOMATED UNIVERSITY REGISTRATION PORTAL VALIDATION SYSTEM")
    print("=" * 80)

    validation_results = [validator.validate_student(s) for s in students_test_data]

    for i, r in enumerate(validation_results, 1):
        print(f"\n[Applicant {i}: {r['name']}]")
        for field, val in r['data'].items():
            if field == "name":
                continue
            err = r['errors'].get(field)
            status_label = "[VALID]" if not err else f"[INVALID] -> {err}"
            print(f"  {field.replace('_', ' ').title():<18}: {val:<25} {status_label}")
        print(f"  Final Decision    : {r['status']}")

    print("\n" + "=" * 80)
    print("                   FINAL REGISTRATION STATUS AUDIT REPORT")
    print("=" * 80)
    print(f"{'Student Name':<22} | {'Register No':<14} | {'Course':<8} | {'Errors':<8} | {'Final Status'}")
    print("-" * 80)
    for r in validation_results:
        err_cnt = len(r['errors'])
        print(f"{r['name']:<22} | {r['data']['reg_no']:<14} | {r['data']['course_code']:<8} | {err_cnt:<8} | {r['status']}")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment()
