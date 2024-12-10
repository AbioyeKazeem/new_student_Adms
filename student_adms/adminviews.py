from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, AdmittedCandidate, CourseRegistration
from .serializers import CandidateSerializer, AdmittedCandidateSerializer, CourseRegistrationSerializer
import logging

logger = logging.getLogger(__name__)


class ApplicationStatusView(APIView):
    """
    View to fetch the status of all applications.
    """
    def get(self, request):
        try:
            candidates = Candidate.objects.all()
            serializer = CandidateSerializer(candidates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching application statuses: {e}")
            return Response({"message": "Error fetching application statuses."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageAdmissionListView(APIView):
    """
    View to manage the admission list.
    """
    def get(self, request):
        try:
            admitted_candidates = AdmittedCandidate.objects.all()
            serializer = AdmittedCandidateSerializer(admitted_candidates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching admission list: {e}")
            return Response({"message": "Error fetching admission list."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, candidate_id):
        try:
            admitted_candidate = AdmittedCandidate.objects.get(id=candidate_id)
            admitted_candidate.delete()
            return Response({"message": "Candidate removed from the admission list."}, status=status.HTTP_200_OK)
        except AdmittedCandidate.DoesNotExist:
            logger.warning(f"Candidate with ID {candidate_id} not found.")
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting candidate: {e}")
            return Response({"message": "Error removing candidate from the admission list."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CourseRegistrationListView(APIView):
    """
    View to list all course registration requests pending approval.
    """
    def get(self, request):
        try:
            # Fetch pending registrations
            registrations = CourseRegistration.objects.filter(approved=False)
            serializer = CourseRegistrationSerializer(registrations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching course registrations: {e}")
            return Response({"message": "Error fetching course registrations."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ApproveCourseRegistrationView(APIView):
    """
    View to approve course registration requests.
    """
    def post(self, request, registration_id):
        try:
            # Log all existing registration IDs for debugging
            logger.debug(f"All CourseRegistration IDs: {[reg.id for reg in CourseRegistration.objects.all()]}")
            
            # Log the provided registration ID from the request
            logger.debug(f"Provided registration_id: {registration_id}")

            # Validate and fetch the registration
            logger.info(f"Attempting to approve registration ID: {registration_id}")
            registration = CourseRegistration.objects.get(id=registration_id)

            # Update the registration status
            registration.approved = True
            registration.save()
            logger.info(f"Registration ID {registration_id} approved successfully.")
            return Response({"message": f"Registration ID {registration_id} approved successfully."}, status=status.HTTP_200_OK)

        except CourseRegistration.DoesNotExist:
            logger.warning(f"CourseRegistration with ID {registration_id} not found.")
            return Response({"error": f"Registration with ID {registration_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Unexpected error while approving registration ID {registration_id}: {e}")
            return Response({"error": "Unexpected server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
