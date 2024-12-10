import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdmissionForm, AdmittedCandidate

# Configure logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=AdmissionForm)
def create_admitted_candidate(sender, instance, created, **kwargs):
    # Only run when a new AdmissionForm is created, not on updates
    if not created:
        return
    
    # Check if the admission status is 'Approved'
    if instance.program_of_choice == 'Approved':  # Assuming you use program_of_choice for approval
        logger.info(f"Admission for {instance.id} approved, creating AdmittedCandidate.")
        # Create the associated AdmittedCandidate
        AdmittedCandidate.objects.create(
            candidate=instance,
            programme=instance.program_of_choice,  # Linking program_of_choice as the candidate's programme
            matric_number=None  # Will be generated later
        )
