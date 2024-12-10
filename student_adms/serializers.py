from rest_framework import serializers
from .models import (
    AdmissionForm,
    CBTQuestion,
    CandidateSubmission,
    Candidate,
    AdmittedCandidate,
    Course,
    CourseRegistration,
)


# AdmissionForm Serializer
class AdmissionFormSerializer(serializers.ModelSerializer):
    """
    Handles the logic and validation for AdmissionForm.
    """
    class Meta:
        model = AdmissionForm
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'gender',
            'state_of_origin', 'program_of_choice', 'parent_guardian_name',
            'parent_guardian_phone', 'birth_certificate', 'academic_transcripts',
            'medical_fitness_report',
        ]


# CBTQuestion Serializer
class CBTQuestionSerializer(serializers.ModelSerializer):
    """
    Handles logic related to CBTQuestion operations.
    """
    class Meta:
        model = CBTQuestion
        fields = ['id', 'question_text', 'options', 'correct_answer']


# CandidateSubmission Serializer
class CandidateSubmissionSerializer(serializers.ModelSerializer):
    """
    Handles submission logic related to candidate answers and scoring.
    """
    class Meta:
        model = CandidateSubmission
        fields = ['id', 'candidate_name', 'candidate_email', 'submitted_answers', 'score', 'submitted_at']


# Candidate Serializer
class CandidateSerializer(serializers.ModelSerializer):
    """
    Handles Candidate-related data serialization and validation logic.
    """
    class Meta:
        model = Candidate
        fields = [
            'id', 'full_name', 'cbt_score', 'utme_score', 'application_details',
            'interview_score', 'health_status_valid', 'admission_status'
        ]


# AdmittedCandidate Serializer
class AdmittedCandidateSerializer(serializers.ModelSerializer):
    """
    Handles logic for admitted candidates' processing.
    """
    full_name = serializers.CharField(source="candidate.full_name", read_only=True)

    class Meta:
        model = AdmittedCandidate
        fields = [
            'id', 'full_name', 'programme', 'admission_year', 'serial_number', 'matriculation_number'
        ]


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    """
    Handles logic for course data serialization.
    """
    class Meta:
        model = Course
        fields = [
            'id', 'course_code', 'course_name', 'programme', 'level', 'description'
        ]


# CourseRegistration Serializer
class CourseRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles serialization logic for CourseRegistration data.
    """
    registration_date = serializers.DateField()  # Force serialization as a date

    class Meta:
        model = CourseRegistration
        fields = ['id', 'admitted_candidate', 'course', 'registration_date', 'approved']

    def to_representation(self, instance):
        """
        Ensure registration_date is serialized as 'YYYY-MM-DD'.
        """
        data = super().to_representation(instance)
        if instance.registration_date:  # Safeguard against None values
            data['registration_date'] = instance.registration_date.strftime('%Y-%m-%d')
        return data
