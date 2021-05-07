from rest_framework import serializers
from .models import AttendanceData, AttendanceModel
import io
from rest_framework.parsers import JSONParser


class AttendanceSerializer(serializers.Serializer):

	id = serializers.IntegerField()
	emp = serializers.CharField(max_length = 100)
	image = serializers.ImageField()
	encod_image = serializers.CharField(max_length = 2500)
	

	
class AttendanceDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = AttendanceData
		fields = '__all__'

	

