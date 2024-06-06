from celery import Celery

from server.src.helpers import google_image_search

app = Celery("ImageProcessTask",
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0'
             )


@app.task
def get_search_images_url(search_text: str, max_urls: int):
    return google_image_search(search_text, max_urls)


@app.task
def download_images(images_url: list[str], temp_folder_path: str):
    return save_images_from_url(images_url, temp_folder_path)
