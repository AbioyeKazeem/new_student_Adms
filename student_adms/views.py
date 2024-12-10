from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AdmissionFormSerializer,
    CBTQuestionSerializer,
    CandidateSubmissionSerializer,
    CandidateSerializer,
    AdmittedCandidateSerializer,
    CourseSerializer,
    CourseRegistrationSerializer
)
from .models import CBTQuestion, CandidateSubmission, Candidate, AdmittedCandidate, Course, CourseRegistration
from .adminviews import ApplicationStatusView, ManageAdmissionListView, ApproveCourseRegistrationView
from .utils import generate_matriculation_number
import logging

logger = logging.getLogger(__name__)


# Application submission views
class ApplicationSubmissionView(APIView):
    """
    Handles submission of application forms.
    """
    def post(self, request):
        serializer = AdmissionFormSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error saving application: {str(e)}")
                return Response({"message": f"Error saving application: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CBT question view
class CBTQuestionView(APIView):
    """
    Handles fetching CBT questions.
    """
    def get(self, request):
        try:
            questions = CBTQuestion.objects.all()
            serializer = CBTQuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching CBT questions: {str(e)}")
            return Response({"message": f"Failed to retrieve CBT questions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# CBT submission view
class CBTSubmissionView(APIView):
    """
    Handles CBT submissions from candidates.
    """
    def post(self, request):
        serializer = CandidateSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "CBT submission successful."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error saving CBT submission: {str(e)}")
                return Response({"message": f"Failed to save CBT submission: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admission list view
class AdmissionListView(APIView):
    """
    Handles listing of all admissions.
    """
    def get(self, request):
        try:
            admissions = Candidate.objects.filter(admitted=True)
            serializer = CandidateSerializer(admissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching admission list: {str(e)}")
            return Response({"message": "An error occurred while fetching the admission list."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdmissionApprovalView(APIView):
    """
    Handles approving candidates for admission.
    """
    def post(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.admitted = True
            candidate.save()
            serializer = CandidateSerializer(candidate)
            return Response({"message": "Candidate approved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            logger.error("Candidate for approval not found.")
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error during admission approval: {str(e)}")
            return Response({"message": "An error occurred during admission approval."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Matriculation number view
class MatriculationNumberView(APIView):
    """
    Handles generating and assigning matriculation numbers.
    """
    def post(self, request):
        programme = request.data.get("programme")
        candidate_id = request.data.get("id")

        if not programme or not candidate_id:
            return Response(
                {"error": "Both 'programme' and 'id' fields must be provided and non-empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            candidate = AdmittedCandidate.objects.get(id=candidate_id)
            last_serial_number = AdmittedCandidate.objects.filter(
                programme=programme, matriculation_number__isnull=False
            ).count() + 1
            matric_number = generate_matriculation_number(programme, last_serial_number)

            candidate.matriculation_number = matric_number
            candidate.save()

            serializer = AdmittedCandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except AdmittedCandidate.DoesNotExist:
            logger.error(f"Candidate with ID {candidate_id} not found.")
            return Response(
                {"error": f"Candidate with ID {candidate_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error in MatriculationNumberView while assigning matriculation: {str(e)}")
            return Response(
                {"error": "An error occurred while assigning the matriculation number."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Course view
class CourseCreationView(APIView):
    """
    Handles creating new courses.
    """
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Course created successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating course: {str(e)}")
                return Response({"message": f"An error occurred while creating the course: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Course registration view
class CourseRegistrationView(APIView):
    """
    Handles course registrations for admitted candidates.
    """
    def post(self, request):
        admitted_candidate_id = request.data.get('admitted_candidate_id')
        course_id = request.data.get('course_id')

        if not admitted_candidate_id or not course_id:
            return Response(
                {"error": "Both 'admitted_candidate_id' and 'course_id' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            admitted_candidate = AdmittedCandidate.objects.get(pk=admitted_candidate_id)
        except AdmittedCandidate.DoesNotExist:
            logger.error(f"Admitted candidate with ID {admitted_candidate_id} not found.")
            return Response({"error": "Admitted candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            logger.error(f"Course with ID {course_id} not found.")
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        if CourseRegistration.objects.filter(admitted_candidate=admitted_candidate, course=course).exists():
            return Response(
                {"error": "This candidate is already registered for the course."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registration = CourseRegistration.objects.create(
                admitted_candidate=admitted_candidate,
                course=course
            )
            return Response(
                {"message": "Course registered successfully.", "registration_id": registration.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Unexpected error during course registration: {str(e)}")
            return Response(
                {"error": "An unexpected database error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
