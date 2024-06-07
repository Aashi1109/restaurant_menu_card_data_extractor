from celery import Celery

from server.src.config import TEMP_FOLDER_PATH, CELERY_BACKEND, CELERY_BROKER
from server.src.database import get_db
from server.src.logger import logger
from server.src.ocr.ocr import perform_ocr
from server.src.scrap.crud import update_task
from server.src.scrap.enums import TaskStatus
from server.src.scrap.helpers import (
    google_image_search_using_selenium, save_images_from_url,
    google_search_using_cse_papi,
)
from server.src.scrap.utils import filter_cse_images_results

app = Celery(
    "ImageProcessTask",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

# Configure Celery to use the existing logger
app.conf.update(
    worker_hijack_root_logger=False,  # Prevent Celery from hijacking the root logger
    worker_log_format="%(message)s",
    worker_task_log_format="%(task_name)s: %(message)s",
)

# Ensure the logger configuration is passed to the workers
app.conf.update(
    worker_redirect_stdouts_level='INFO',
    worker_log_color=False,
)


@app.task(name="scrap_results")
def scrap_save_search_results_worker(search_text: str, max_urls: int, use_cse_papi: bool, metadata):
    try:
        logger.info(f"Scrapping data. metadata: {str(metadata)}")
        scraped_images_url = []
        if use_cse_papi:
            search_results = google_search_using_cse_papi(search_text, max_urls)

            filtered_results = filter_cse_images_results(search_results)
            scraped_images_url = [x['link'] for x in filtered_results]
        else:
            scraped_images_url = google_image_search_using_selenium(search_text, max_urls)

        saved_images_path = download_images_worker(scraped_images_url, metadata)

        # get ocr results
        ocr_results = ocr_worker(saved_images_path, metadata)

        if ocr_results:
            if "db" in metadata:
                task_id = metadata["db"]["id"]
                scrap_data = "\n\n\n".join(ocr_results)
                update_task(get_db(), task_id, scrap_data=scrap_data, status=TaskStatus.Completed)
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            with get_db() as session:
                update_task(session, task_id, status=TaskStatus.Failed)


@app.task(name="download_images")
def download_images_worker(images_url: list[str], metadata):
    try:
        logger.info(f"Scrapping data. metadata: {str(metadata)}")

        return save_images_from_url(images_url, TEMP_FOLDER_PATH)
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            with get_db() as session:
                update_task(session, task_id, status=TaskStatus.Failed)


@app.task(name="ocr")
def ocr_worker(images_path: list[str], metadata):
    try:
        ocr_results = []

        for image_path in images_path:
            ocr_result = perform_ocr(image_path)
            if ocr_result:
                ocr_results.append(ocr_result)

        return ocr_results
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            with get_db() as session:
                update_task(session, task_id, status=TaskStatus.Failed)
