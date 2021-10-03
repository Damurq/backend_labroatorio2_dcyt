from rest_framework import serializers
from pensum.models import *

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class PensumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pensum
        fields = '__all__'

class ProgramPensumSerializer(serializers.ModelSerializer):
    program_code= ProgramSerializer()

    class Meta:
        model = Pensum
        fields = '__all__'

class CountSerializer(serializers.Serializer):
    name_Pro = serializers.CharField(max_length=255)
    count = serializers.IntegerField()