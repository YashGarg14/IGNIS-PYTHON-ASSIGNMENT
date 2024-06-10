from celery import shared_task
from .models import ScrapingTask, ScrapingJob
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(task_id):
    task = ScrapingTask.objects.get(id=task_id)
    task.status = 'IN_PROGRESS'
    task.save()

    data = CoinMarketCap.fetch_coin_data(task.coin)
    task.data = data
    task.status = 'COMPLETED' if data else 'FAILED'
    task.save()
