import os
import time
import urllib.parse
import urllib.request
import uuid

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def google_image_search(query: str, num_images: int):
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

        for thumbnail in thumbnails[:num_images]:
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
                        break  # Break after finding the first valid image URL
            except Exception as e:
                print(f"Error: {e}")
                continue

        return list(set(image_urls))
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if driver: driver.quit()


def save_images_from_url(images_url: list[str], temp_folder_path: str):
    try:
        images_url = [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjuQKlsvrlg4V3tENCWaJXejnxGn_vmd-4JA&s"
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdJePsygmChsWDEHXKVprnJoYIQVdL9Q23Sg&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbhzzxjpkPMYC9APqyWhMhbWrXlXVXczuIog&s",
            "https://media-cdn.tripadvisor.com/media/photo-s/05/33/03/88/britannia-co.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCGPLi_jUygVY-VVyeP1_OYljMV3fqsZkNJA&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAJNFoToc6C_PNE0LkIOEPKWl8_8fiX3Nq3A&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxVReKWpfOgTlrVex52WkoF83C8LWJuxYfJQ&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvBnP8j72bR2PpQUzCXmV81LcZenMVYJfGGg&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiMeU9yW_68-E9co3DaR8bEaX_gXbLtmBIHQ&s",
        ]

        file_saved_paths = []
        for image_url in images_url:
            file_saved_path = save_image_from_url(image_url, temp_folder_path)
            file_saved_paths.append(file_saved_path)

        return file_saved_paths
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def save_image_from_url(image_url: str, save_folder_path: str, stream_save=True, filename=None):
    try:
        if not filename:
            filename = uuid.uuid4().__str__() + ".png"
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
            print(f"Failed to retrieve image. HTTP Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


# save_image_from_url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjuQKlsvrlg4V3tENCWaJXejnxGn_vmd-4JA&s",
#                     r"D:\Coding\internship\image_scrapper\temp")

def google_search_using_cse_papi(search_query: str, max_links: int):
    try:
        # get the minimum amount of links to fetch
        min_per_search_results_link = min(10, max_links)
        cse_id = "e74ae2f61bea249ef"
        api_key = "AIzaSyDYgOOODO_MHGrV28sIRPdrQ9GIaZlX4dU"
        url = (f"https://www.googleapis.com/customsearch/v1?q={search_query}&num={min_per_search_results_link}&start=1"
               f"&imgSize=huge&searchType=image&key={api_key}&cx={cse_id}")

        response = requests.get(url)
        response.raise_for_status()

        search_results = response.json()
        if "items" in search_results:
            extracted_items = search_results["items"]
            return extracted_items
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


# print(save_images_from_url([], r"D:\Coding\internship\image_scrapper\temp"))
print(google_search_using_cse_papi("mumbai restaurant menu card", 20))