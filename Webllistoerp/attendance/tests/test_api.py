from tastypie.test import ResourceTestCaseMixin
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from attendance.serializers import AttendanceSerializer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from attendance.views import DataCollection, PostCollection
from core.models import CustomUser



# class EntryResourceTest(ResourceTestCaseMixin, TestCase):

# 	def setUp(self):
# 		super(EntryResourceTest, self).setUp()
# 		self.d = Client()
# 		self.api_url = reverse('data_collection')

# 	def test_get_api_json(self):
# 		resp = self.api_client.get(self.api_url, format='json')
# 		self.assertValidJSONResponse(resp)
# 		self.assertEqual(resp.status_code, 200)

# 	def test_post_api_invalid_json(self):
# 		self.data = {
# 						"timestamp" : "10-Apr-2021 (10:30:35.263131)",
# 						"emp_id"    :  73,
# 						"emp"       :  "alban_sheikh"
# 					}
# 		self.serializer_class = AttendanceSerializer
# 		serializer = self.serializer_class(data = self.data)
# 		self.assertFalse(serializer.is_valid())



# class AttendanceApiTest(APITestCase):

# 	def setUp(self):
# 		self.factory = APIRequestFactory()
# 		# self.view = apiviews.PollViewSet.as_view({'get': 'list'})
# 		self.api_url = reverse('data_collection')

# 	def test_attendance_api(self):
# 		request = self.factory.get(self.uri)
# 		response = self.view(request)	



class AttendanceDataCollectionApiTest(APITestCase):

	def setUp(self):
		self.factory = APIRequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('data_collection')

	def test_attendancge_data_collection(self):
		request = self.factory.get(self.attendance_url)
		request.user = self.member
		response = DataCollection.as_view()(request)
		self.assertEqual(response.status_code, 200)

class AttendancePostCollectionApiTest(APITestCase):

	def setUp(self):
		self.factory = APIRequestFactory()
		self.attendance_url = reverse('post_collection')

	def test_attendancge_data_collection(self):
		data =  {
    				"timestamp" : "10-Apr-2021 (10:30:35.263131)",
    				"emp_id" : 73,
    				"emp" :  "alban_sheikh"
				}
		request = self.factory.post(self.attendance_url, data)
		response = PostCollection.as_view()(request)
		self.assertEqual(response.status_code, 400)
