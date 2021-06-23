from tastypie.test import ResourceTestCaseMixin
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from attendance.serializers import AttendanceSerializer



class EntryResourceTest(ResourceTestCaseMixin, TestCase):

	def setUp(self):
		super(EntryResourceTest, self).setUp()
		self.d = Client()
		self.api_url = reverse('data_collection')

	def test_get_api_json(self):
		resp = self.api_client.get(self.api_url, format='json')
		self.assertValidJSONResponse(resp)
		self.assertEqual(resp.status_code, 200)

	def test_post_api_invalid_json(self):
		self.data = {
						"timestamp" : "10-Apr-2021 (10:30:35.263131)",
						"emp_id"    :  73,
						"emp"       :  "alban_sheikh"
					}
		self.serializer_class = AttendanceSerializer
		serializer = self.serializer_class(data = self.data)
		self.assertFalse(serializer.is_valid())

    