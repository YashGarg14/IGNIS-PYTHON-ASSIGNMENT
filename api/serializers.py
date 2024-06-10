from rest_framework import serializers
from .models import ScrapingJob, ScrapingTask

class CryptoRequestSerializer(serializers.Serializer):
    acronyms = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )

    def validate_acronyms(self, value):
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError("All items must be strings.")
        return value

class ScrapingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingTask
        fields = ['coin', 'data', 'status']

class ScrapingJobSerializer(serializers.ModelSerializer):
    tasks = ScrapingTaskSerializer(many=True)

    class Meta:
        model = ScrapingJob
        fields = ['id', 'tasks']
