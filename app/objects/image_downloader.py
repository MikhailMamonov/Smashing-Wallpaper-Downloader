import re
import os 
import requests
import asyncio
import aiohttp
import aiofiles
from typing import List
from bs4 import BeautifulSoup


class ImageDownloader:

    def __init__(self, resolution:str):
        self.resolution = self.validate_input(resolution)
    
    @staticmethod
    def validate_input(resolution: str) -> str:
        match = re.search('^\d{3,4}x\d{3,4}$', resolution)
        if match:
            return resolution
        raise ValueError('Resolution value is not valid', resolution)
    
    def get_url(self, base_url:str, year: int, month_number: int, month_name: str)-> str:

        # (month_number-1) and form '01', '02',.., '12'
        month_number_str = str(range(1, 13)[month_number-2])
        if len(month_number_str) == 2:
            converted_month_number = month_number_str
        else:
            converted_month_number = '0{0}'.format(month_number_str)
        
        year_category = (year-1) if converted_month_number == '12' else year

        url = 'https://{0}/{1}/{2}/desktop-wallpaper-calendars-{3}-{4}/'.format(
            base_url,
            year_category, 
            converted_month_number,
            month_name.lower(), 
            year
        )

        return url
    
    def create_directory(self, basic_directory: str, month_name: str, year:int) -> str:
        storage_path = os.path.join(
            basic_directory, 
            'Smashing_wallpaper_{0}_{1}'.format(month_name, year)
            )
        try:
            os.makedirs(storage_path, exist_ok=True)
        except OSError as err:
            raise Exception('Unable to create directory for downloading files: {}'.format(err))
        else:
            return storage_path
    
    def fetch_content(self, url: str, **kwargs) -> bytes:
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
        except requests.Timeout:
            raise Exception('Connection time out')
        except requests.HTTPError:
            raise Exception('Error {}'.format(response.status_code))
        except requests.RequestException:
            raise Exception('Unable to establish connection')
        else:
            return response.content
        
    def get_image_links(self, content: bytes)-> List[str]:
        soup = BeautifulSoup(content, 'lxml')
        image_links = []

        for link in soup.find_all('a'):
            if link.text == self.resolution:
                image_links.append(link.get('href'))
        return image_links
    
    async def download_image(self,session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, storage_path: str, link: str)-> bool:
        try:
            async with semaphore:
                async with session.get(link) as response:
                    response.raise_for_status()
                    image_name = link[link.rfind('/')+1:]
                    async with aiofiles.open(
                        os.path.join(storage_path, image_name), 
                        mode='wb'
                    ) as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk: 
                                break
                            await f.write(chunk)
        except Exception:
            return False
        else:
            return True

    
    async def download_all(self, storage_path:str, links: List[str]) -> int:
        download_image_count = 0
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.download_image(
                session, semaphore, storage_path, link)) for link in links]
            for res in asyncio.as_completed(tasks):
                result = await res
                if result:
                    download_image_count+=1
        return download_image_count


        
    
    