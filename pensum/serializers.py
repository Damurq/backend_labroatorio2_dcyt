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
