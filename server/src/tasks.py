from celery import Celery

from server.src.scrap.helpers import google_image_search_using_selenium, save_images_from_url, \
    google_search_using_cse_papi
from server.src.scrap.utils import filter_cse_images_results

app = Celery("ImageProcessTask",
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0'
             )


@app.task
def scrap_get_search_results_scheduler(search_text: str, max_urls: int, use_cse_papi: bool, metadata: Any):
    scraped_images_url = []
    if use_cse_papi:
        search_results = google_search_using_cse_papi(search_text, max_urls)

        filtered_results = filter_cse_images_results(search_results)
        scraped_images_url = [x['link'] for x in filtered_results]
    else:
        scraped_images_url = google_image_search_using_selenium(search_text, max_urls)

    download_images(scraped_images_url)


@app.task
def download_images(images_url: list[str], temp_folder_path: str):
    return save_images_from_url(images_url, temp_folder_path)
