from pathlib import Path
from typing import Any

import scrapy
from scrapy.http import Response


class ImageScrapper(scrapy.Spider):
    name = 'image_scrapper'

    def start_requests(self):
        url = [
            "https://www.google.com/search?tbm=isch&q=mumbai%20restaurant%20menu%20images"]
        for u in url:
            yield scrapy.Request(url=u, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        page = response.url.split("/")[-2]
        filename = f'restaurant-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f"Saved filename: {filename}")
