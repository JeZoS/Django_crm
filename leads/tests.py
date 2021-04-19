from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.
class LandingPageTest(TestCase):
    def test_get(self):
        res = self.client.get(reverse('landing-page'))
        self.assertEqual(res.status_code,200)