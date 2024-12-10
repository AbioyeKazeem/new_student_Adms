from django.test import TestCase
from .models import AdmittedCandidate
from .utils import generate_matriculation_number

class MatriculationNumberTests(TestCase):
    def test_generate_matriculation_number(self):
        matric_number = generate_matriculation_number("Doctor of Physiotherapy", 17)
        self.assertEqual(matric_number, "DPT/2024/017")

    def test_matriculation_number_view(self):
        # Create a test candidate
        candidate = AdmittedCandidate.objects.create(
            full_name="John Doe",
            programme="Doctor of Physiotherapy"
        )

        # Make a POST request
        response = self.client.post('/generate-matric-number/', {
            "programme": "Doctor of Physiotherapy",
            "candidate_id": candidate.id
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn("matriculation_number", response.data)
