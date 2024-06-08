from celery import Celery

from server.src.SessionLocal import get_db_context
from server.src.config import TEMP_FOLDER_PATH, CELERY_BACKEND, CELERY_BROKER
from server.src.logger import logger
from server.src.ocr.ocr import perform_ocr
from server.src.scrap.crud import update_task
from server.src.scrap.enums import TaskStatus
from server.src.scrap.helpers import (
    google_image_search_using_selenium, save_images_from_url,
    google_search_using_cse_papi,
)
from server.src.scrap.utils import filter_cse_images_results

celery_app = Celery(
    __name__,
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

celery_app.conf.update(worker_hijack_root_logger=False)


# # Configure Celery to use the existing logger
# celery_app.conf.update(
#     # worker_hijack_root_logger=False,  # Prevent Celery from hijacking the root logger
#     worker_log_format="%(message)s",
#     worker_task_log_format="%(task_name)s: %(message)s",
# )
#
# # Ensure the logger configuration is passed to the workers
# celery_app.conf.update(
#     worker_redirect_stdouts_level='INFO',
#     worker_log_color=False,
# )


# @after_setup_logger.connect
# def setup_celery_logging(logger, **kwargs):
#     logger.info("Celery worker started")


@celery_app.task(name="scrap_results")
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

        logger.info(f"Images url extracted: {scraped_images_url}")
        saved_images_path = download_images_worker(scraped_images_url, metadata)

        logger.info(f"Image saved: {saved_images_path}")
        logger.info(f"Performing OCR on downloaded images results")
        # get ocr results
        ocr_results = ocr_worker(saved_images_path, metadata)
        logger.info(f"OCR results extracted: {ocr_results}")

        if ocr_results:
            if "db" in metadata:
                task_id = metadata["db"]["id"]
                scrap_data = "\n\n\n".join(ocr_results)
                logger.info("Updating task status to completed after successfully extracting text from images")
                with get_db_context() as session:
                    update_task(session, task_id, scrap_data=scrap_data, status=TaskStatus.Completed)
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            logger.warning("Task failed updating task status to failed")

            with get_db_context() as session:
                update_task(session, task_id, status=TaskStatus.Failed)


@celery_app.task(name="download_images")
def download_images_worker(images_url: list[str], metadata):
    try:
        logger.info(f"Downloading images metadata: {str(metadata)}")

        return save_images_from_url(images_url, TEMP_FOLDER_PATH)
    except Exception as e:
        logger.error(f"Error scraping data: {str(e)}", exc_info=True)
        #  update status of task as failed
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            logger.warning("Task failed updating task status to failed")
            with get_db_context() as session:
                update_task(session, task_id, status=TaskStatus.Failed)


@celery_app.task(name="ocr")
def ocr_worker(images_path: list[str], metadata):
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
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            logger.warning("Task failed updating task status to failed")
            with get_db_context() as session:
                update_task(session, task_id, status=TaskStatus.Failed)
