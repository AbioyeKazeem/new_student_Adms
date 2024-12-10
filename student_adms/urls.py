from django.urls import path

# Importing the main views
from .views import (
    ApplicationSubmissionView,
    CBTQuestionView,
    CBTSubmissionView,
    AdmissionListView,
    AdmissionApprovalView,
    MatriculationNumberView,
    CourseCreationView,
    CourseRegistrationView
)

# Importing admin views
from .adminviews import (
    ApplicationStatusView,
    ManageAdmissionListView,
    CourseRegistrationListView,
    ApproveCourseRegistrationView
)


urlpatterns = [
    # Application endpoints
    path('submit-application/', ApplicationSubmissionView.as_view(), name='submit-application'),
    
    # CBT endpoints
    path('cbt-questions/', CBTQuestionView.as_view(), name='cbt-questions'),
    path('submit-cbt/', CBTSubmissionView.as_view(), name='submit-cbt'),

    # Admission endpoints
    path('admission-list/', AdmissionListView.as_view(), name='admission-list'),
    path('admission-approval/<int:candidate_id>/', AdmissionApprovalView.as_view(), name='admission-approval'),
    path('generate-matric-number/', MatriculationNumberView.as_view(), name='generate-matric-number'),

    # Course endpoints
    path('add-course/', CourseCreationView.as_view(), name='add-course'),
    path('register-course/', CourseRegistrationView.as_view(), name='register-course'),

    # Admin functions
    path('admin/applications/', ApplicationStatusView.as_view(), name='application_status'),
    path('admin/admissions/', ManageAdmissionListView.as_view(), name='manage_admissions'),
    path('admin/admissions/<int:candidate_id>/', ManageAdmissionListView.as_view(), name='remove_admission'),
    # Separate list view for course registrations
    path('admin/course-registrations/', CourseRegistrationListView.as_view(), name='list_course_registrations'),
    # Separate approve endpoint for individual registration approvals
    path('admin/course-registrations/<int:registration_id>/approve/', ApproveCourseRegistrationView.as_view(), name='approve_course_registration'),
]
