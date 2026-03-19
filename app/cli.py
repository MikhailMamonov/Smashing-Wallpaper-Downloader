from app.parser import parse_args
from constants.api import *
from app.objects.date import Date
from app.objects.image_downloader import ImageDownloader
import asyncio



def run_cli():
    args = parse_args()
    try:
        date = Date(args.my)
        downloader = ImageDownloader(args.resolution)
    except ValueError as err: 
        message, value = err.args
        print('{0}: {1}'.format(message, value))
        return
    
    #Getting url link in expected format
    url = downloader.get_url(URL, date.year, date.month_number, date.month_name)

    #Making GET request, creating storage directory for images,
    try:
        storage_path = downloader.create_directory(BASE_URL, date.month_name, date.year)
        content = downloader.fetch_content(url, timeout=5) 
    except Exception as err:
        print(err)
        return 
    else:
        image_links = downloader.get_image_links(content)
        if not image_links:
            print('Unable to download images witn given parameters.')
            return
    
    print('Connection established, start downloading...')

    downloaded_image_count = asyncio.run(
        downloader.download_all(storage_path, image_links))
    
    if downloaded_image_count:
        print('\nDownload complete. Downloaded {} images.'.format(downloaded_image_count))
    else:
        print('Unified issues occured while attempting to download images')


    
    



