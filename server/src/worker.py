import os

from celery import Celery

from server.src.config import TEMP_FOLDER_PATH, CELERY_BACKEND, CELERY_BROKER
from server.src.logger import logger
from server.src.ocr.ocr import perform_ocr
from server.src.scrap.enums import TaskStatus
from server.src.scrap.helpers import (
    google_image_search_using_selenium, save_images_from_url,
    google_search_using_cse_papi, update_task_from_metadata,
)
from server.src.scrap.utils import filter_cse_images_results

celery_app = Celery(
    __name__,
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

celery_app.conf.update(worker_hijack_root_logger=True)

celery_app.conf.broker_transport_options = {
    'retry_policy': {
        'timeout': 5.0
    }
}
celery_app.conf.result_backend_transport_options = {
    'retry_policy': {
        'timeout': 5.0
    },

}

celery_app.conf.broker_connection_retry_on_startup = True


@celery_app.task(name="scrap_results")
def scrap_save_search_results_worker(search_text: str, max_urls: int, use_cse_papi: bool, metadata):
    """
    Performs scraping of search results, downloads images, performs OCR on them, and updates task status accordingly.
    :param search_text: Text to search for
    :param max_urls: Maximum number of URLs to fetch
    :param use_cse_papi: Flag indicating whether to use CSE PAPI for search
    :param metadata: Additional metadata for the task
    """
    try:
        logger.info(f"Scrapping data. metadata: {str(metadata)}")
        scraped_images_url = []
        if use_cse_papi:
            search_results = google_search_using_cse_papi(search_text, max_urls)
            filtered_results = filter_cse_images_results(search_results)
            scraped_images_url = [x['link'] for x in filtered_results]
        else:
            scraped_images_url = google_image_search_using_selenium(search_text, max_urls)

        logger.info(f"Images url extracted: {scraped_images_url}")
        saved_images_path = download_images_worker(scraped_images_url, metadata)

        logger.info(f"Image saved: {saved_images_path}")
        logger.info(f"Performing OCR on downloaded images results")
        # get ocr results
        ocr_results = ocr_worker(saved_images_path, metadata)
        logger.info(f"OCR results extracted: {ocr_results}")

        if ocr_results:
            scrap_data = "\n\n\n".join(ocr_results)
            update_task_from_metadata(metadata, TaskStatus.Completed, scrap_data)

            # remove downloaded files
            logger.info(f"Removing downloaded images")
            for image_path in saved_images_path:
                if image_path: os.remove(image_path)

    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        update_task_from_metadata(metadata, task_status=TaskStatus.Failed)


@celery_app.task(name="download_images")
def download_images_worker(images_url: list[str], metadata):
    """
    Downloads images from provided URLs and updates task status accordingly.
    :param images_url: List of URLs of images to download
    :param metadata: Additional metadata for the task
    """
    try:
        logger.info(f"Downloading images metadata: {str(metadata)}")

        return save_images_from_url(images_url, TEMP_FOLDER_PATH)
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        update_task_from_metadata(metadata, task_status=TaskStatus.Failed)


@celery_app.task(name="ocr")
def ocr_worker(images_path: list[str], metadata):
    """
    Performs OCR on downloaded images and updates task status accordingly.
    :param images_path: List of paths to downloaded images
    :param metadata: Additional metadata for the task
    """
    try:
        logger.info(f"Performing OCR on downloaded images metadata: {str(metadata)}")
        ocr_results = []

        for image_path in images_path:
            ocr_result = perform_ocr(image_path)
            if ocr_result:
                ocr_results.append(ocr_result)

        return ocr_results
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        update_task_from_metadata(metadata, task_status=TaskStatus.Failed)
