from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CryptoRequestSerializer, ScrapingJobSerializer
from .models import ScrapingJob, ScrapingTask
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request):
        serializer = CryptoRequestSerializer(data=request.data)
        if serializer.is_valid():
            acronyms = serializer.validated_data['acronyms']
            job = ScrapingJob.objects.create()
            for acronym in acronyms:
                task = ScrapingTask.objects.create(job=job, coin=acronym)
                scrape_coin_data.delay(task.id)
            return Response({'job_id': job.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapingJob.objects.get(id=job_id)
        except ScrapingJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
