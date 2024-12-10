# New Student Admission Management System (AdMS)
The New Student Admission Management System (AdMS) backend provides endpoints to manage school admissions, applications, course registration, CBTs, and other administrative workflows.

# Setup Instructions
1.	Clone Repository
git clone <repository-url>
cd <repository-directory>
2.	Apply Migrations
python manage.py migrate
3.	Start Development Server
python manage.py runserver

# API Endpoints
Application Endpoints
These endpoints handle the submission of university applications.
•	Submit Application 
	URL: /submit-application/
	Method: POST
	Description: Submit a university application.

# CBT Endpoints
These endpoints manage the handling and submission of CBT questions and answers.
•	Retrieve CBT Questions
	URL: /cbt-questions/
	Method: GET
	Description: Retrieve CBT questions.
•	Submit CBT Response
	URL: /submit-cbt/
	Method: POST
	Description: Submit a CBT response.

# Admission Endpoints
These endpoints manage admissions, matriculation number generation, and applicant approvals.

•	List Admission Candidates
	URL: /admission-list/
	Method: GET
	Description: List all admission candidates.
•	Approve Admission
	URL: /admission-approval/<candidate_id>/
	Method: POST
	Description: Approve an applicant's admission.
•	Generate Matriculation Number
	URL: /generate-matric-number/
	Method: POST
	Description: Generate a matriculation number for approved applicants.

# Course Endpoints
These endpoints allow the creation of courses and student course registration.
•	Create Course
	URL: /add-course/
	Method: POST
	Description: Create a new course.
•	Register for Course
	URL: /register-course/
	Method: POST
	Description: Register for a selected course.

# Admin Functions
Administrative endpoints allow managing applications, admissions, and course registrations.
•	View All Applications
	URL: /admin/applications/
	Method: GET
	Description: View all submitted applications.
•	View Admitted Candidates
	URL: /admin/admissions/
	Method: GET
	Description: View list of admitted candidates.
•	Remove Admission
	URL: /admin/admissions/<candidate_id>/
	Method: DELETE
	Description: Remove an admission for a candidate.
•	View Course Registrations Pending Approval
	URL: /admin/course-registrations/
	Method: GET
	Description: View all course registration requests pending approval.
•	Approve Course Registration
	URL: /admin/course-registrations/<registration_id>/approve/
	Method: POST
	Description: Approve a specific course registration.

# Testing with Postman
To test the API using Postman, ensure you use the proper Content-Type header for all requests with JSON payloads.
1.	Submit Application
	URL: http://localhost:8000/submit-application/
	Method: POST

3.	CBT Submission
	URL: http://localhost:8000/submit-cbt/
	Method: POST

5.	Admission Approval
	URL: http://localhost:8000/admission-approval/1/
	Method: POST

7.	Course Registration
	URL: http://localhost:8000/register-course/
	Method: POST

9.	Approve Course Registration
	URL: http://localhost:8000/admin/course-registrations/1/approve/
	Method: POST

# Content-Type Header
For all requests involving JSON payloads, include the following header:
•	Key: Content-Type
•	Value: application/json
This ensures compatibility and proper payload submission for the endpoints.

# Note: The database named Adms is inside the student_adms project directory, feel free to get it installed through any method of your choice.


