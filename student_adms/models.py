from django.db import models


class AdmissionForm(models.Model):
    id = models.BigAutoField(primary_key=True)  
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    state_of_origin = models.CharField(max_length=50)
    program_of_choice = models.CharField(max_length=100)
    parent_guardian_name = models.CharField(max_length=255)
    parent_guardian_phone = models.CharField(max_length=15)
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/', blank=True, null=True)
    academic_transcripts = models.FileField(upload_to='documents/academic_transcripts/', blank=True, null=True)
    medical_fitness_report = models.FileField(upload_to='documents/medical_reports/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class CBTQuestion(models.Model):
    question_text = models.TextField()
    options = models.JSONField()  # JSON field to store options as a list
    correct_answer = models.CharField(max_length=255)  # Store the correct answer as a string

    def __str__(self):
        return self.question_text


class CandidateSubmission(models.Model):
    candidate_name = models.CharField(max_length=255)
    candidate_email = models.EmailField()
    submitted_answers = models.JSONField()  # JSON field to store answers as a dictionary
    score = models.FloatField(null=True, blank=True)  # Store score after grading
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name


class Candidate(models.Model):
    full_name = models.CharField(max_length=255)
    cbt_score = models.FloatField()
    utme_score = models.FloatField()
    application_details = models.JSONField()  # Store application info like submitted files
    interview_score = models.FloatField()
    health_status_valid = models.BooleanField()  # True if medical fitness report is valid
    admission_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )

    def __str__(self):
        return self.full_name


class AdmittedCandidate(models.Model):
    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='admitted_candidate'
    )
    programme = models.CharField(max_length=100)
    admission_year = models.IntegerField()  # Represents the year the candidate was admitted
    serial_number = models.IntegerField(unique=True, default=1)  
    matriculation_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.matriculation_number}"
    

class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    level = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"



class CourseRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    admitted_candidate = models.ForeignKey(AdmittedCandidate, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.admitted_candidate} - {self.course}"

