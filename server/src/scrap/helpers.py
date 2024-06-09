import os
import time
import urllib.parse
import urllib.request
import uuid
from http.client import HTTPException
from typing import Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from server.src.SessionLocal import get_db_context
from server.src.config import GOOGLE_CSE_ID, GOOGLE_API_KEY
from server.src.logger import logger
from server.src.scrap.crud import update_task
from server.src.scrap.enums import TaskStatus


def google_image_search_using_selenium(query: str, num_images: int):
    """
    Extracts images url using selenium and chromium
    :param query: Search query
    :param num_images: NUmber of images to fetch
    :return: Images url retrieved
    """
    driver = None
    try:
        # Setup Chrome webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run headless Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?tbm=isch&q={query}"
        driver.get(url)

        # Scroll down to load more images
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # clickable images are present in a certain div
        # get that div and then click on other images
        images_div = driver.find_element(By.CSS_SELECTOR, "div.wH6SXe.u32vCb")

        if not images_div:
            return []

        # Find image elements
        thumbnails = images_div.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
        image_urls = []

        for thumbnail in thumbnails:
            try:
                # get top div parent and perform click on it
                parent_div = thumbnail.find_element(By.XPATH, './ancestor::div[1]')
                if not parent_div:
                    continue
                parent_div.click()
                time.sleep(1)
                actual_images = driver.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc')
                for actual_image in actual_images:
                    src = actual_image.get_attribute('src')
                    if src and 'http' in src:
                        image_urls.append(src)

                if len(image_urls) >= num_images:
                    break
            except Exception as e:
                logger.error(f"Error: {e}")
                continue

        return list(set(image_urls))
    except Exception as e:
        logger.error(f"Error: {e}")
        return []
    finally:
        if driver:
            driver.quit()


def save_images_from_url(images_url: list[str], temp_folder_path: str):
    """
    Saves images to a temporary folder
    :param images_url: List of images url to save
    :param temp_folder_path: Folder to save images to
    :return: Local path of images where they are saved
    """
    try:
        file_saved_paths = []
        for image_url in images_url:
            try:
                file_saved_path = save_image_from_url(image_url, temp_folder_path)
                file_saved_paths.append(file_saved_path)
            except HTTPException:
                continue

        return file_saved_paths
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []


def get_uuid4():
    return uuid.uuid4().__str__()


def save_image_from_url(image_url: str, save_folder_path: str, stream_save=True, filename=None):
    """
    Saves image to a temporary folder
    :param image_url: URL of image to save
    :param save_folder_path: Folder where to save the image
    :param stream_save: To use streaming download or single shot download
    :param filename: Name to save the image with
    :return: Full path to the saved image
    """
    try:
        if not filename:
            filename = get_uuid4() + ".png"
        file_path = os.path.join(save_folder_path, filename)
        # Send a GET request to the image URL with streaming
        response = requests.get(image_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a local file in binary write mode
            with open(file_path, 'wb') as file:
                if stream_save:
                    # Write the image data to the file in chunks
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                else:
                    # Write the entire image data to the file in one go
                    file.write(response.content)
            return file_path
        else:
            logger.warning(f"Failed to retrieve image. HTTP Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


def google_search_using_cse_papi(search_query: str, max_links: int, start: int = 1, collected_links: list = None):
    """
    Uses CSE and Google Programmable Search API to search for images
    :param search_query: Search Query
    :param max_links: Maximum links to try to fetch
    :param start: Index of search results
    :param collected_links: List containing search results data
    :return: Extracted results
    """
    if collected_links is None:
        collected_links = []

    try:
        # Calculate the number of results to fetch in this request
        results_to_fetch = min(10, max_links - len(collected_links))

        # API credentials and endpoint
        cse_id = GOOGLE_CSE_ID
        api_key = GOOGLE_API_KEY
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            'q': search_query,
            'num': results_to_fetch,
            'start': start,
            'imgSize': 'huge',
            'searchType': 'image',
            'key': api_key,
            'cx': cse_id
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        search_results = response.json()
        if "items" in search_results:
            collected_links.extend(search_results["items"])

        # If we haven't collected enough links, make another recursive call
        if len(collected_links) < max_links:
            next_start = start + results_to_fetch
            return google_search_using_cse_papi(
                search_query, max_links, start=next_start,
                collected_links=collected_links
            )

        return collected_links
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def update_task_from_metadata(metadata, task_status: TaskStatus, scrap_data: Optional[str] = None):
    """
    Updates task status from metadata
    :param metadata: Task metadata
    :param scrap_data: Scrap data
    :param task_status: Task status
    :return: None
    """
    try:
        if "db" in metadata:
            task_id = metadata["db"]["id"]
            with get_db_context() as session:
                logger.info(f"Updating task with task_id:{task_id} to {task_status.value}")
                update_task(session, task_id, status=task_status, scrap_data=scrap_data)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
